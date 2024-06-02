from sqlalchemy.orm.session import Session

from ..models.user_and_chat import UserAndChat
from ..models.user_and_guild import UserAndGuild
from ..models.user import User
from .common import session_handler


UserEntity = User | UserAndChat | UserAndGuild


@session_handler
def get(id: int, session: Session | None = None) -> User | None:
    return session.query(User).get(id)


@session_handler
def get_by_username(username: str, session: Session | None = None) -> User | None:
    return session.query(User).filter_by(username=username).one_or_none()


@session_handler
def get_all(user_ids: list[int] | None = None,
            usernames: list[str] | None = None,
            session: Session | None = None) -> list[User]:
    """Get users entries associated with provided filters or whole table instead

    :param list[int] | None user_ids: user ids, defaults to None (skip this filter)
    :param list[str] | None usernames: usernames, defaults to None (skip this filter)
    :param Session | None session: database connection session, defaults to None
    :return list[User]: users table entries
    """
    query = session.query(User)

    if user_ids:
        query = query.filter(User.id.in_(user_ids))
    if usernames:
        query = query.filter(User.username.in_(usernames))

    return query.all()


@session_handler
def update(users: list[UserEntity], session: Session | None = None):
    session.add_all(users)


@session_handler
def delete(user: UserEntity | list[UserEntity], session: Session | None = None):
    users = user if isinstance(user, list) else [user]
    for cur_user in users:
        session.delete(cur_user)
