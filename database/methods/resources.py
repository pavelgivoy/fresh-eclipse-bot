from sqlalchemy.orm.session import Session

from . import captures, guild
from .common import session_handler, get_empty_id, get_query_from_intervals
from ..models.alliance import Alliance
from ..models.guild import Guild
from ..models.resources import Resource
from ..models.location import Location


@session_handler
def get_all(location_ids: list[int | None] = None,
            types: list[str | None] = None,
            names: list[str | None] = None,
            price_interval: list[int] | None = None,
            select_resources: bool = False,
            select_buffs: bool = False,
            session: Session | None = None) -> list[Resource]:
    """Get resources entries associated with provided filters, or whole table instead

    :param list[int] location_ids: location ids, defaults to None (skip this filter)
    :param list[str] types: item types (resource, magic item, glory, buff), defaults to None (skip this filter)
    :param list[str] names: item names (Magic Stone, Ruby, forge buff name, etc.), defaults to None (skip this filter)
    :param list[int] price_interval: interval of mines/glory points buff prices, defaults to None (skip this filter)
    :param bool select_resources: add only resources entries, defaults to False (skip this filter)
    :param bool select_buffs: add only buffs entries, defaults to False (skip this filter)
    :param Session session: database connection session, defaults to None (session will be opened when the function is called and closed when the function is completed)
    :return list[Resource]: resources table entries
    """
    query = session.query(Resource)

    if location_ids:
        query = query.filter(Resource.location_id.in_(location_ids))
    if types:
        query = query.filter(Resource.type.in_(types))
    if names:
        query = query.filter(Resource.name.in_(names))
    if price_interval is not None:
        query = get_query_from_intervals(Resource.price, price_interval)

    if select_resources:
        query = query.filter(Resource.price == None)
    elif select_buffs:
        query = query.filter(Resource.price != None)

    return query.all()


@session_handler
def get_capture_info(capture: Alliance | Location, session: Session | None = None) -> dict[str, None | str | int | list[Guild] | list[Resource]]:
    ans = {'owner': None, 'life_time': None, 'owned_time': None,
           'points': None, 'guilds': None, 'resources': None, 'buffs': None}

    ans['name'] = capture.name
    if isinstance(capture, Alliance):
        ans["owner"] = capture.owner or "неизвестно"
        ans["guilds"] = guild.get_all(alliances=[capture.id],
                                      session=session)
        ans["points"] = capture.points
    if isinstance(capture, Location):
        owner = captures.get(capture.owner, session=session).name
        ans["owner"] = owner
        ans["resources"] = get_all(location_ids=[capture.id],
                                   select_resources=True,
                                   session=session)
        ans["buffs"] = get_all(location_ids=[capture.id],
                               select_buffs=True,
                               session=session)
        ans["life_time"] = capture.life_time
        ans["owned_time"] = capture.owned_time
    return ans


def get_empty_resource_id(session: Session | None = None) -> int:
    resources = session.query(Resource).all()
    return get_empty_id(resources)


@session_handler
def update(location: Location, resources: list[str], buff: str, price: int, session: Session | None = None):
    if resources:
        found_resources = get_all(location_ids=[location.id],
                                  select_resources=True,
                                  session=session)
        if found_resources:
            delete(found_resources, session=session)
        for resource in resources:
            new_resource = Resource(id=get_empty_resource_id(session=session),
                                    location_id=location.id,
                                    type='resource',
                                    name=resource)
            session.add(new_resource)
    if buff and price:
        found_buffs = get_all(location_ids=[location.id],
                              types=['buff'],
                              names=[buff])
        if found_buffs:
            found_buff = found_buffs[0]
            found_buff.price = price
        else:
            new_buff = Resource(id=get_empty_resource_id(session=session),
                                location_id=location.id,
                                type='buff',
                                name=buff,
                                price=price)
        session.add(new_buff)


@session_handler
def delete(resources: list[Resource], session: Session | None = None):
    for resource in resources:
        session.delete(resource)
