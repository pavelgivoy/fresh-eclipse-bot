from sqlalchemy import Column, or_
from sqlalchemy.orm.session import Session

from .common import session_handler
from ..models.trigger import Trigger


@session_handler
def get(id: int, session: Session | None = None) -> Trigger | None:
    return session.query(Trigger).get(id)


@session_handler
def get_by_name(name: str, chat_id: int, session: Session | None = None) -> Trigger | None:
    return session.query(Trigger) \
        .filter_by(name=name) \
        .filter_by(chat_id=chat_id) \
        .one_or_none()


@session_handler
def get_all(column: Column | None = None,
            ids: list[int] | None = None,
            chat_ids: list[int] | None = None,
            message_ids: list[int] | None = None,
            names: list[str] | None = None,
            text_values: list[str] | None = None,
            file_ids: list[str] | None = None,
            strict: bool | None = None,
            session: Session | None = None) -> list[Trigger]:
    """Get trigger entries associated with provided filters or whole table instead

    :param Column | None column: column name, defaults to None
    :param list[int] | None ids: trigger ids to search, defaults to None
    :param list[int] | None chat_ids: chat ids, defaults to None
    :param list[int] | None message_ids: message ids, defaults to None
    :param list[str] | None names: trigger names, defaults to None
    :param list[str] | None text_values: saved message text or caption, defaults to None
    :param list[str] | None file_ids: saved triggers file id, defaults to None
    :param bool | None strict: filter by strict, defaults to None
    :param Session | None session: database connection session, defaults to None
    :return list[Trigger]: trigger table entries
    """

    column = column or Trigger
    query = session.query(column)

    if ids:
        query = query.filter(Trigger.id.in_(ids))
    if chat_ids:
        if None in chat_ids:
            chat_ids.remove(None)
            # None in [None] == False for sqlalchemy in_() method
            query = query.filter(or_(
                Trigger.chat_id.is_(None),
                Trigger.chat_id.in_(chat_ids)
            ))
        else:
            query = query.filter(Trigger.chat_id.in_(chat_ids))
    if message_ids:
        query = query.filter(Trigger.message_id.in_(message_ids))
    if names:
        query = query.filter(Trigger.name.in_(names))
    if text_values:
        query = query.filter(Trigger.text_value.in_(text_values))
    if file_ids:
        query = query.filter(Trigger.file_id.in_(file_ids))
    if strict is not None:
        query = query.filter(Trigger.strict == strict)

    return query.all()


@session_handler
def add(trigger_type: str,
        chat_id: int,
        message_id: int,
        name: str,
        text_value: str | None,
        file_id: str | None,
        strict: bool,
        session: Session | None = None):
    trigger = Trigger(type=trigger_type,
                      chat_id=chat_id,
                      message_id=message_id,
                      name=name,
                      text_value=text_value,
                      file_id=file_id,
                      strict=strict)
    session.add(trigger)


@session_handler
def edit(trigger: Trigger,
         trigger_type: str,
         message_id: int,
         text_value: str | None,
         file_id: str | None,
         strict: bool,
         session: Session | None = None):
    trigger.type = trigger_type
    trigger.message_id = message_id
    trigger.text_value = text_value
    trigger.file_id = file_id
    trigger.strict = strict
    session.add(trigger)


@session_handler
def delete(trigger: Trigger,
           session: Session | None = None):
    session.delete(trigger)
