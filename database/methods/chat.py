from sqlalchemy import Column
from sqlalchemy.orm.session import Session

from .common import session_handler
from ..models.chat import Chat
from ..models.user_and_chat import UserAndChat
from utils.game_staff.chatset_translating import settings_translating_reversed, status_from_key


@session_handler
def get(id: int, session: Session | None = None) -> Chat | None:
    """Get chat sequence from group chat id

    :param int id: chat id (filtering object)
    :param Session | None session: database connection session, defaults to None
    :return Chat | None: found sequence
    """
    return session.query(Chat).get(id)


@session_handler
def get_chat_from_group_chat_id(id: int, session: Session | None = None) -> Chat | None:
    """Get chat sequence from group chat id

    :param int id: chat id (filtering object)
    :param Session | None session: database connection session, defaults to None
    :return Chat | None: found sequence
    """
    return session.query(Chat).get(id)


@session_handler
def get_chat_from_user(user_id: int,
                       chats: list[Chat],
                       groups: list[str] | bool | None = None,
                       guilds: list[str] | bool | None = None,
                       alliances: list[str] | bool | None = None,
                       single_guild: bool = False,
                       single_alliance: bool = False,
                       session: Session | None = None):
    filtered_chats = chats
    filtered_chat_ids = list(map(lambda chat: chat.id, filtered_chats))
    user_chat_ids = session.query(UserAndChat.chat_id) \
        .filter_by(user_id=user_id) \
        .filter(UserAndChat.chat_id.in_(filtered_chat_ids)) \
        .all()
    user_chat_ids = list(map(lambda chat_id: chat_id[0], user_chat_ids))
    filtered_chats = list(
        filter(lambda chat: chat.id in user_chat_ids, filtered_chats))

    # if guilds and alliances are specified, their exact matches are required
    chat_guilds = set(map(lambda chat: chat.guild, filtered_chats))
    if single_guild and len(chat_guilds) > 1:
        return 'multiple_guilds_found'
    chat_alliances = set(map(lambda chat: chat.alliance, filtered_chats))
    if single_alliance and len(chat_alliances) > 1:
        return 'multiple_alliances_found'

    if isinstance(groups, list):
        # if multiple groups found, select the most important one
        # alliance and guild chats cannot be super chats
        # guild chats can be allowed chats only
        match_group = 'super' if 'super' in groups and not guilds and not alliances \
            else 'war' if 'war' in groups and not guilds \
            else 'admin' if 'admin' in groups and not guilds \
            else 'allowed' if 'allowed' in groups else None
        filtered_chats = list(filter(lambda chat: chat.group == match_group,
                                     filtered_chats))
    return filtered_chats[-1] if filtered_chats else None


@session_handler
def get_chat_info(obj_id: int,
                  groups: list[str] | bool | None = None,
                  guilds: list[str] | bool | None = None,
                  alliances: list[str] | bool | None = None,
                  single_guild: bool = False,
                  single_alliance: bool = False,
                  triggers_allowed: bool | None = None,
                  session: Session | None = None):
    query = session.query(Chat)
    if isinstance(groups, list):
        query = query.filter(Chat.group.in_(groups))
    elif groups:
        query = query.filter(Chat.group != None)

    if isinstance(guilds, list):
        query = query.filter(Chat.guild.in_(guilds))
    elif guilds:
        query = query.filter(Chat.guild != None)

    if isinstance(alliances, list):
        query = query.filter(Chat.alliance.in_(alliances))
    elif alliances:
        query = query.filter(Chat.alliance != None)

    if triggers_allowed is not None:
        query = query.filter(Chat.triggers_allowed == triggers_allowed)

    # obj_id >= 0 is for user id and obj_id < 0 is for chat id
    found_chat = get_chat_from_user(obj_id,
                                    query.all(),
                                    groups=groups,
                                    guilds=guilds,
                                    alliances=alliances,
                                    single_guild=single_guild,
                                    single_alliance=single_alliance,
                                    session=session) if obj_id >= 0 \
        else query.filter_by(id=obj_id).one_or_none()
    return found_chat


def get_group(chat: Chat | None):
    return 'not allowed' if chat is None else chat.group


def get_locations_review_allowed(chat: Chat | None):
    return False if chat is None else chat.locations_review_allowed


@session_handler
def get_all(column: Column | None = None,
            chat_ids: list[int] | None = None,
            groups: list[str] | None = None,
            guilds: list[str] | None = None,
            alliances: bool | list[int] | None = None,
            locations_review_allowed: bool | None = None,
            triggers_allowed: bool | None = None,
            withdrawing_allowed: bool | None = None,
            session: Session | None = None) -> list[Chat]:
    column = column or Chat
    query = session.query(column)

    if chat_ids:
        query = query.filter(Chat.id.in_(chat_ids))
    if groups:
        query = query.filter(Chat.group.in_(groups))
    if guilds:
        query = query.filter(Chat.guild.in_(guilds))
    if isinstance(alliances, list):
        query = query.filter(Chat.alliance.in_(alliances))
    elif alliances:
        query = query.filter(Chat.alliance != None)
    if locations_review_allowed is not None:
        query = query.filter(Chat.locations_review_allowed ==
                             locations_review_allowed)
    if triggers_allowed is not None:
        query = query.filter(Chat.triggers_allowed == triggers_allowed)
    if withdrawing_allowed is not None:
        query = query.filter(Chat.withdrawing_allowed == withdrawing_allowed)

    return query.all()


@session_handler
def add(chat_id: int, group: str,
        guild: str | None, alliance_id: int | None,
        session: Session | None = None):
    chat = Chat(id=chat_id, group=group, guild=guild, alliance=alliance_id)
    session.add(chat)


@session_handler
def delete(chat: Chat, session: Session | None = None):
    chats = chat if isinstance(chat, list) else [chat]
    for cur_chat in chats:
        session.delete(cur_chat)


@session_handler
def edit(chat: Chat, settings: list[str], session: Session | None = None):
    for i in range(2, len(settings)):
        chatset, status = settings[i].split(': ')
        chatset = settings_translating_reversed[chatset]
        status = status_from_key[status]
        chat.__setattr__(chatset, status)

    session.add(chat)
    return 'edited'
