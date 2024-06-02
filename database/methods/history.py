import datetime

from sqlalchemy import or_
from sqlalchemy.orm.session import Session

from ..models.history import History
from .common import get_empty_id, session_handler, get_query_from_intervals
from .captures import get_by_code, get_by_name


@session_handler
def get(hist_id: int, session: Session | None = None) -> History:
    return session.query(History).get(hist_id)


@session_handler
def get_all(ids: list[int] | None = None,
            capture_ids: list[int] | None = None,
            date_interval: list[datetime.datetime] | None = None,
            results: list[str] | None = None,
            stocks: list[int] | None = None,
            glory: list[int] | None = None,
            owners: list[int] | None = None,
            session: Session | None = None) -> list[History]:
    query = session.query(History)

    if ids:
        query = query.filter(History.id.in_(ids))
    if capture_ids:
        query = query.filter(or_(
            History.alliance_id.in_(capture_ids),
            History.location_id.in_(capture_ids)
        ))
    if date_interval:
        query = get_query_from_intervals(History.date, date_interval)
    if results:
        query = query.filter(History.result.in_(results))
    if stocks:
        query = get_query_from_intervals(History.stock, stocks)
    if glory:
        query = get_query_from_intervals(History.glory, glory)
    if owners:
        query = query.filter(History.owner.in_(owners))
    return query.all()


def get_empty_history_id(session: Session) -> int:
    posts = session.query(History.id).all()
    return get_empty_id(posts)


@session_handler
def add_alliance(date: datetime.datetime, alliance_id: int, alliance_entry: dict[str, int | str | None], session: Session | None = None):
    post_id = get_empty_history_id(session)
    entry = History(id=post_id,
                    date=date,
                    alliance_id=alliance_id,
                    result=alliance_entry['result'],
                    stock=alliance_entry['stock'],
                    glory=alliance_entry['glory'])
    update(entry, session=session)


@session_handler
def add_location(date: datetime.datetime, location_id: int, location_entry: dict[str, int | str | None], session: Session | None = None):
    post_id = get_empty_history_id(session)
    entry = History(id=post_id,
                    date=date,
                    location_id=location_id,
                    result=location_entry['result'],
                    owner=location_entry['new_owner'])
    update(entry, session=session)


@session_handler
def update(entry: History, session: Session | None = None):
    session.add(entry)


@session_handler
def update_location_owner(code: str, battle_date: datetime.datetime, new_owner: str, session: Session | None = None):
    capture = get_by_code(code, session=session)
    if not capture:
        return 'capture_not_found'

    history_entries = get_all(capture_ids=[capture.id],
                              date_interval=[battle_date, battle_date],
                              session=session)
    if not history_entries:
        return 'history_not_found'

    new_owner_alliance = get_by_name(new_owner, session=session)
    if not new_owner_alliance:
        return 'owner_not_found'
    capture.owner = new_owner_alliance.id

    last_entry = history_entries[-1]
    last_entry.owner = new_owner_alliance.id
    session.add(last_entry)
