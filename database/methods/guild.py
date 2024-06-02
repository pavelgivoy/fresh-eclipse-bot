from sqlalchemy.orm.session import Session
from database.models.alliance import Alliance

from utils.game_staff.basic_hq import BASIC_HQ_ID

from .common import session_handler, get_query_from_intervals
from .captures import get_by_code
from ..models.guild import Guild
from . import chat


@session_handler
def get(tag: str, session: Session | None = None) -> Guild | None:
    return session.query(Guild).get(tag)


@session_handler
def get_by_name(name: str, session: Session | None = None) -> Guild | None:
    return session.query(Guild).filter(Guild.name == name).one_or_none()


def get_found_and_omited_guilds(args: list[str]) -> tuple[list[Guild], list[str]]:
    """Select concrete guilds from basic alliance and filter abscent guilds

    :param list[str] args: guild tags which should be searched in the database
    :return tuple[list[Guild], list[str]]: found guild entries list and omited guild tags list
    """
    guilds = get_all(alliances=[BASIC_HQ_ID])
    guild_tags = list(map(lambda guild: guild.tag, guilds))
    omited_guilds = list(filter(lambda arg: arg not in guild_tags, args))
    found_guilds = list(filter(lambda guild: guild.tag in args,
                               guilds)) or guilds
    return found_guilds, omited_guilds


@session_handler
def get_all(tags: list[str] | None = None,
            names: list[str] | None = None,
            level_interval: int | list[int] | None = None,
            emojis: list[str] | None = None,
            castles: list[str] | None = None,
            alliances: list[int] | None = None,
            glory_interval: int | list[int] | None = None,
            session: Session | None = None) -> list[Guild]:
    """Get guilds entries associated with provided filters, or whole table instead

    :param list[str] | None tags: guild tags, defaults to None (skip this filter)
    :param list[str] | None names: guild names, defaults to None (skip this filter)
    :param int | list[int] | None level_interval: guild level interval, defaults to None (skip this filter)
    :param list[str] | None emojis: guild emojis, defaults to None (skip this filter)
    :param list[str] | None castles: castle emojis, defaults to None (skip this filter)
    :param list[int] | None alliances: alliance ids, defaults to None (skip this filter)
    :param int | list[int] | None glory_interval: guild glory stats interval, defaults to None (skip this filter)
    :param Session | None session: database connection session, defaults to None (session will be opened when the function is called and closed when the function is completed)
    :return list[Guild]: guilds table entries
    """
    query = session.query(Guild)

    if tags:
        query = query.filter(Guild.tag.in_(tags))
    if names:
        query = query.filter(Guild.name.in_(names))
    if level_interval is not None:
        query = get_query_from_intervals(Guild.level, level_interval)
    if emojis:
        query = query.filter(Guild.emoji.in_(emojis))
    if castles:
        query = query.filter(Guild.castle.in_(castles))
    if alliances:
        query = query.filter(Guild.alliance.in_(alliances))
    if glory_interval is not None:
        query = get_query_from_intervals(Guild.glory, glory_interval)

    return query.all()


@session_handler
def set_alliance_owner(code: str, guild_tag: str, session: Session | None = None):
    alliance = get_by_code(code, session=session)
    if not alliance:
        return 'alliance_not_found'

    guild = get(guild_tag, session=session)
    if not guild:
        return 'guild_not_found'

    update_single_guild_alliance_info(guild, alliance.id, session=session)
    alliance.owner = guild.tag
    session.add(alliance)
    return 'added'


@session_handler
def update_single_guild_alliance_info(guild: Guild, alliance_id: int | None, session: Session | None = None):
    guild_chats = chat.get_all(guilds=[guild.tag], session=session)
    for guild_chat in guild_chats:
        guild_chat.alliance = alliance_id
    guild.alliance = alliance_id
    session.add_all([*guild_chats, guild])


@session_handler
def update_guilds_alliance_info(guilds: list[dict[str, str | None]], alliance: Alliance, new_guild_tags: list[str], session: Session | None = None):
    # delete guilds which are apscent in parsed profile
    cur_guilds = get_all(alliances=[alliance.id], session=session)
    for cur_guild in cur_guilds:
        if cur_guild.tag not in new_guild_tags:
            update_single_guild_alliance_info(cur_guild, None, session=session)

    # add new guilds to the found alliance
    for guild_info in guilds:
        cur_guild = get(guild_info['tag'], session=session)
        emoji = None if guild_info['emoji'] == '' else guild_info['emoji']
        if cur_guild:
            cur_guild.name = guild_info['name']
            cur_guild.castle = guild_info['castle']
            cur_guild.emoji = emoji
            update_single_guild_alliance_info(
                cur_guild, alliance.id, session=session)
        else:
            cur_guild = Guild(tag=guild_info['tag'], name=guild_info['name'],
                              castle=guild_info['castle'], emoji=emoji,
                              alliance=alliance.id)
        session.add(cur_guild)


@session_handler
def delete(guild: Guild | list[Guild], session: Session | None = None) -> str:
    guilds = guild if isinstance(guild, list) else [guild]
    for cur_guild in guilds:
        session.delete(cur_guild)
    return 'deleted'


@session_handler
def update(guilds: list[Guild], session: Session | None = None) -> str:
    """update guilds table with new or edited entries

    :param Guild guilds: new or edited guilds table entries
    :param Session | None session: database connection session, defaults to None
    :return str: operation result
    """
    session.add_all(guilds)
    return 'updated'
