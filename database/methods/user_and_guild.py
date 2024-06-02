from sqlalchemy import Column
from sqlalchemy.orm.session import Session

from utils.game_staff.basic_hq import BASIC_HQ_ID
from ..models.user_and_guild import UserAndGuild
from ..models.user import User
from .common import session_handler
from . import guild, user


@session_handler
def get(user_id: int,
        guild: str,
        column: Column[int | str] | None = None,
        session: Session | None = None) -> UserAndGuild:
    column = column or UserAndGuild
    return session.query(column) \
                  .filter_by(user_id=user_id,
                             guild=guild).one_or_none()


@session_handler
def get_all(user_id: int | None = None,
            guild: str | None = None,
            column: Column[int | str] | None = None,
            session: Session | None = None) -> list[UserAndGuild]:
    column = column or UserAndGuild
    query = session.query(column)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if guild:
        query = query.filter_by(guild=guild)
    return query.all()


@session_handler
def add_repr(guild_tag: str,
             user_id: int,
             username: str,
             session: Session | None = None):
    cur_guild = guild.get(guild_tag, session=session)
    if cur_guild.alliance != BASIC_HQ_ID:
        return 'guild_not_found'

    # get user, or create new one, if not exists
    cur_user = user.get(user_id, session=session)
    user_created = False
    if not cur_user:
        cur_user = User(id=user_id, username=username)
        user_created = True

    # get user and guild match
    # return existing one, or create new one otherwise
    cur_user_and_guild = get(user_id=user_id,
                             guild=guild_tag,
                             session=session)
    if cur_user_and_guild:
        return 'repr_found'
    new_user_and_guild = UserAndGuild(user_id=user_id,
                                      guild=guild_tag)

    if user_created:
        session.add(cur_user)
    session.add(new_user_and_guild)


@session_handler
def delete_repr(guild_tag: str,
                user_info: str | int,
                flag: str | None,
                session: Session | None = None):
    cur_guild = guild.get(guild_tag, session=session)
    if not cur_guild or cur_guild.alliance != BASIC_HQ_ID:
        return 'guild_not_found'

    cur_user = user.get(user_info, session=session) if user_info is int \
        else user.get_by_username(user_info, session=session)
    if flag == 'force':
        session.delete(cur_user)
        return 'deleted'
    user_and_guild = get(user_id=cur_user.id,
                         guild=guild_tag,
                         session=session)
    if not user_and_guild:
        return 'repr_not_found'

    session.delete(user_and_guild)
    return 'deleted'
