from sqlalchemy import Column
from sqlalchemy.orm.session import Session

from .common import session_handler, get_query_from_intervals
from ..models.master import Master


@session_handler
def get(link: str, session: Session | None = None):
    return session.query(Master).get(link)


@session_handler
def get_all(links: list[str] | None = None,
            guilds: list[str] | None = None,
            castles: list[str] | None = None,
            usernames: list[str] | None = None,
            bs_gurus: list[str] | None = None,
            bs_level_interval: list[int] | None = None,
            alch_gurus: list[str] | None = None,
            alch_level_interval: list[int] | None = None,
            session: Session | None = None) -> list[Master]:
    """List masters entries associated with provided filters, or whole table instead

    :param list[str] bs_gurus: blacksmith specializations list, defaults to [] (skip this filter)
    :param list[str] bs_level_interval: blacksmith skill level interval, defaults to [] (skip this filter)
    :param list[str] alch_gurus: alchemist specializations list, defaults to [] (skip this filter)
    :param list[str] alch_level_interval: alchemist skill level interval, defaults to [] (skip this filter)
    :return list[Master]: masters table entries
    """
    query = session.query(Master)

    if links:
        query = query.filter(Master.link.in_(links))
    if guilds:
        query = query.filter(Master.guild.in_(guilds))
    if castles:
        query = query.filter(Master.castle.in_(castles))
    if usernames:
        query = query.filter(Master.username.in_(usernames))
    if bs_gurus:
        query = query.filter(Master.bs_guru.in_(bs_gurus))
    # Start and end blacksmith skill level interval must be provided to make search between them
    if bs_level_interval:
        query = get_query_from_intervals(
            query, Master.bs_level, bs_level_interval)
    if alch_gurus:
        query = query.filter(Master.alch_guru.in_(alch_gurus))
    # Start and end alchemist skill level interval must be provided to make search between them
    if alch_level_interval:
        query = get_query_from_intervals(
            query, Master.alch_level, alch_level_interval)

    return query.all()


@session_handler
def update(link: str,
           castle: str,
           username: str,
           guild: str | None = None,
           bs_guru: str | None = None,
           bs_level: int | None = None,
           alch_guru: str | None = None,
           alch_level: str | None = None,
           session: Session | None = None):
    """Add new Masters table entry

    :param str link: shop link
    :param str castle: guru castle
    :param str username: guru username to send requests to open the shop
    :param str guild | None: guru guild, defautls to None (no guild)
    :param str | None bs_guru: blacksmith specialization, if exists, defaults to None (no specialization)
    :param int | None bs_level: blacksmith skill level, if exists, defaults to None (no level)
    :param str | None alch_guru: alchemist specialization, if exists, defaults to None (no specialization)
    :param str | None alch_level: alchemist skill level, if exists, defaults to None (no level)
    """
    master = get(link, session=session)
    if not master:
        master = Master(link=link)

    master.castle = castle
    master.username = username
    master.guild = guild
    master.bs_guru = bs_guru
    master.bs_level = bs_level
    master.alch_guru = alch_guru
    master.alch_level = alch_level
    session.add(master)
    return 'updated'


@session_handler
def delete(link: str,
           session: Session | None = None):
    master = get(link, session=session)
    if not master:
        return 'not_found'
    session.delete(master)
    return 'deleted'
