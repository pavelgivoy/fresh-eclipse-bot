import random
from sqlalchemy.orm.session import Session

from ..models.alliance import Alliance
from ..models.location import Location
from .chat import get_chat_from_group_chat_id
from .common import get_empty_id, session_handler


@session_handler
def get(capture_id: int, session: Session | None = None) -> Alliance | Location | None:
    return session.query(Alliance).get(capture_id) \
        or session.query(Location).get(capture_id)


@session_handler
def get_by_owner_and_name(alliance_id: int, loc_name: str, session: Session | None = None):
    return session.query(Location) \
        .filter(Location.name == loc_name) \
        .filter(Location.owner == alliance_id).all()


@session_handler
def get_all_locations(session: Session | None = None):
    return session.query(Location).all()


@session_handler
def get_all_unknown_locations(session: Session | None = None):
    return session.query(Location) \
        .filter(Location.code.startswith('unknown_')).all()


@session_handler
def get_all_owned_locations(basic_alliance_id: int, session: Session | None = None):
    return session.query(Location) \
        .filter(Location.owner == basic_alliance_id).all()


@session_handler
def get_all_alliances(session: Session | None = None):
    return session.query(Alliance).all()


@session_handler
def get_all_active_alliances(session: Session | None = None):
    return session.query(Alliance) \
        .filter(Alliance.active == True).all()


@session_handler
def get_alliance_by_owner(guild_tags: list[str], session: Session | None = None) -> Alliance | None:
    alliances = get_all_alliances(session=session)
    for alliance in alliances:
        if alliance.owner in guild_tags:
            return alliance
    return None


@session_handler
def get_owner(owner: int, session: Session | None = None):
    """Get owner alliance instance from owner alliance id

    :param int owner: owner alliance id
    :return Alliance: found alliance (it will be always found)
    """
    return session.query(Alliance) \
        .filter(Alliance.id == owner).one()


@session_handler
def get_basic_alliance_info(chat_id: int, session: Session | None = None) -> Alliance | None:
    """Get info about alliance which a chat responds to

    :param int chat_id: group chat id which some alliance can belong to
    :return Alliance | None: found alliance
    """
    chat = get_chat_from_group_chat_id(chat_id)
    if not chat:
        return None
    return session.query(Alliance) \
        .filter(Alliance.id == chat.alliance).one_or_none()


@session_handler
def get_by_name(name: str, session: Session | None = None) -> Alliance | Location | None:
    if 'lvl.' not in name:
        res = session.query(Alliance) \
            .filter(Alliance.name == name).one_or_none()
    else:
        # location names can be multiplied
        # as we don't have quite adequate information of them, we select any random
        locations = session.query(Location) \
            .filter(Location.name == name).all()
        res = locations[random.randint(
            0, len(locations)-1)] if locations else None

    return res


@session_handler
def get_by_code(code: str, session: Session | None = None):
    return session.query(Alliance) \
        .filter(Alliance.code == code).one_or_none() \
        or session.query(Location) \
        .filter(Location.code == code).one_or_none()


def get_empty_capture_id(session: Session):
    captures = session.query(Location.id).all()
    captures.extend(session.query(Alliance.id).all())

    return get_empty_id(captures)


def create_code(id: int) -> str:
    """Create code for new location or alliance if this is undefined

    :param int id: location/alliance id
    :return str: location/alliance code
    """
    return f'unknown_{id}'


@session_handler
def add(id: int, code: str, name: str, session: Session | None = None):
    if 'lvl.' in name:
        loc_type = 'mine' if 'Mine' in name else \
            'ruins' if 'Ruins' in name else 'glory_point'
        capture = Location(id=id, code=code, name=name,
                           type=loc_type, life_time=0, owned_time=0, owner=1)
    else:
        capture = Alliance(id=id, code=code, name=name)
    session.add(capture)
    return capture


@session_handler
def add_single(code: str, name: str, session: Session | None = None) -> str:
    """Add single location or alliance

    :param str code: location/alliance code
    :param str name: location/alliance name
    :return str: operation result
    """
    capture = get_by_code(code, session=session)
    if capture:
        return 'found'
    capture = get_by_name(name, session=session)
    capture_id = get_empty_capture_id(session=session)

    if capture:
        capture.code = code
        session.add()
    else:
        add(capture_id, code, name, session=session)
    return 'added'


@session_handler
def update(captures: list[Alliance | Location], session: Session | None = None):
    session.add_all(captures)


@session_handler
def delete(capture: Alliance | Location, must_be_deleted: bool, session: Session | None = None):
    if isinstance(capture, Alliance) and not must_be_deleted:
        capture.active = not capture.active
        session.add(capture)
        ans = 'not deleted'
    else:
        session.delete(capture)
        ans = 'deleted'
    return ans


@session_handler
def clear_locations(session: Session | None = None):
    locations = session.query(Location).all()
    for location in locations:
        session.delete(location)
    return 'deleted'
