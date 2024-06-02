from aiogram import types
from sqlalchemy import Column
from sqlalchemy.orm.session import Session

from ..models.user_and_chat import UserAndChat
from .common import session_handler


@session_handler
def get(user_id: int,
        chat_id: int,
        column: Column[int] | None = None,
        session: Session | None = None) -> UserAndChat:
    column = column or UserAndChat
    return session.query(column) \
                  .filter_by(user_id=user_id,
                             chat_id=chat_id).one_or_none()


@session_handler
def get_all(user_id: int | None = None,
            chat_id: int | None = None,
            chat_ids: list[int] | None = None,
            column: Column[int] | None = None,
            session: Session | None = None) -> list[UserAndChat]:
    column = column or UserAndChat
    query = session.query(column)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if chat_id:
        query = query.filter_by(chat_id=chat_id)
    if chat_ids:
        query = query.filter(UserAndChat.chat_id.in_(chat_ids))
    return query.all()


@session_handler
def add_user(user_id: int, chat_id: int, is_admin: bool = False, session: Session | None = None):
    new_user_and_chat = UserAndChat(
        user_id=user_id, chat_id=chat_id, is_admin=is_admin)
    session.add(new_user_and_chat)
    return 'added'


@session_handler
def delete(user_id: int, chat_id: int, session: Session | None = None):
    user_and_chat = get(user_id, chat_id, session=session)
    session.delete(user_and_chat)


Admins = types.ChatMemberOwner | types.ChatMemberAdministrator


@session_handler
def add_admins(admins: list[Admins], chat_id: int, session: Session | None = None):
    admins = [UserAndChat(user_id=admin.user.id,
                          chat_id=chat_id,
                          is_admin=True)
              for admin in admins]
    session.add_all(admins)
    return 'added'
