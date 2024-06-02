import datetime
import random
import re

from copy import deepcopy
from sqlalchemy import not_
from sqlalchemy.orm.session import Session

from utils.game_staff.battle_reports import battle_report
from ..models.chat import Chat
from ..models.location import Location
from . import captures, history
from .common import session_handler


@session_handler
def write(date: datetime.datetime,
          parsed_hq_report: list[dict[str, str | int | None]],
          parsed_map_report: list[dict[str, str | int | None]],
          session: Session | None = None):
    for entry in parsed_hq_report:
        # get info about current alliance from db
        alliance = captures.get_by_name(entry['name'], session=session)
        # if db doesn't contain this alliance, create new one
        if not alliance:
            capture_id = captures.get_empty_capture_id(session=session)
            code = captures.create_code(capture_id)
            captures.add(capture_id,
                         code, entry['name'],
                         session=session)
        # else get its id
        else:
            capture_id = alliance.id
        # finally add new entry into history table
        history.add_alliance(date, capture_id,
                             entry, session=session)

    # list of processed locations to exclude history entries duplicating
    # duplicated names may be excepted as reports can be read only by names
    checked_locations = []
    for entry in parsed_map_report:
        # get info about current location from db
        # no warranty about what is current location,
        # as db can store more than one location with same name
        # so filter locations with same name which was processed earlier
        locations = session.query(Location) \
            .filter(Location.name == entry['name']) \
            .filter(Location.id.not_in(checked_locations)).all()
        # if db doesn't contain this location, create new one
        if not locations:
            capture_id = captures.get_empty_capture_id(session=session)
            code = captures.create_code(capture_id)
            location = captures.add(capture_id,
                                    code, entry['name'],
                                    session=session)
        # else get any random id
        # TODO try to analyze location migrations and modify info in-place
        else:
            location = locations[random.randint(0, len(locations)-1)]
            capture_id = location.id

        # store info about selected old_owner to reuse it to send messages to chats
        entry['old_owner'] = location.owner

        # update location related info
        location.seen = True
        location.life_time += 1
        # owner is None means that owner didn't change
        # and other case means that location has new owner
        if entry['new_owner'] is None:
            location.owned_time += 1
        else:
            owner = captures.get_by_name(entry['new_owner'], session=session)
            if not owner:
                owner = captures.add(capture_id,
                                     captures.create_code(capture_id),
                                     entry['new_owner'],
                                     session=session)
            location.owner = owner.id
            location.owned_time = 0
        # update location entry
        session.add(location)
        # add history entry
        history_entry = deepcopy(entry)
        history_entry['new_owner'] = captures.get(location.owner,
                                                  session=session).name
        history.add_location(date, capture_id, history_entry,
                             session=session)
        # mark location as checked
        checked_locations.append(capture_id)
    return 'added'


@session_handler
def include_owners(text: str, session: Session | None = None) -> dict[int, str]:
    """Insert info related to owners of current alliance into common report

    :param str text: initial report text of results lines with structure:
    {result} {name} {grabbed items/new owner}
    :return str: formatted report text which includes owner related info with structure: {alliance oriented result}{standard result} {name} {grabbed items/new owner}
    :param Session | None session: database connection session, defaults to None
    :return dict[int, str]: dictionary with generated modified texts related to alliance id keys
    """
    # alliances for which text should be modified to show related info
    required_alliances = session.query(Chat.alliance).distinct() \
        .filter(Chat.alliance != None).all()
    texts = {}
    for alliance in required_alliances:
        cur_alliance = captures.get(alliance)
        # (id,) -> id to correct keys in texts dictionary
        alliance = alliance[0]
        map_report = False
        lines = text.splitlines(keepends=True)
        loc_num = 0  # locations number checked while lines reading
        for i in range(len(lines)):
            prefix = ''
            line_text = lines[i]
            if 'State of Map' in line_text:
                map_report = True
                continue
            if not map_report and cur_alliance.name in line_text:
                prefix = '✔️' if re.search(r'[😴👌]', line_text, flags=re.UNICODE) \
                    else '✅' if '🛡' in line_text else '❌'
            elif map_report and cur_alliance.name in line_text:
                lines[i-1] = '✅' + lines[i-1]
            elif map_report and 'lvl.' in line_text:
                if battle_report.parsed_map_report[loc_num]['old_owner'] == alliance:
                    prefix = '✔️' if re.search(r'[😴👌]', line_text, flags=re.UNICODE) \
                        else '✅' if '🛡' in line_text else '❌'
                loc_num += 1
            lines[i] = prefix + lines[i]
        texts[alliance] = ''.join(lines)
    return texts
