from sqlalchemy.orm.session import Session

from .common import get_empty_id, session_handler
from ..models.request import Request


@session_handler
def get(id: int, session: Session | None = None) -> Request | None:
    return session.query(Request).get(id)


@session_handler
def get_by_text(text: str, session: Session | None = None):
    """Find request with given text

    :param Session session: database connection session
    :param str text: request text
    :return list[Request]: list of found requests
    """
    return session.query(Request) \
        .filter(Request.text == text).one_or_none()


@session_handler
def get_all(session: Session | None = None) -> list[Request]:
    return session.query(Request).all()


def get_empty_request_id(session: Session) -> int:
    posts = session.query(Request.id).all()
    return get_empty_id(posts)


@session_handler
def add(text: str, session: Session | None = None):
    new_id = get_empty_request_id(session)
    request = Request(id=new_id, text=text)
    session.add(request)


@session_handler
def delete(request: Request, session: Session | None = None):
    session.delete(request)


@session_handler
def edit(request: Request, text: str, session: Session | None = None):
    request.text = text
    session.add(request)
