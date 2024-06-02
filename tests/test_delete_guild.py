import unittest
import datetime

from sqlalchemy import func
from sqlalchemy.orm.session import Session

from database.models.guild import Guild
from database.models.chat import Chat
from database.models.user import User
from database.models.user_and_guild import UserAndGuild
from database.models.user_and_chat import UserAndChat
from database.methods.common import session_handler

cur_time = datetime.datetime.now()

test_guild_tag = 'TST'
test_guild_name = 'Test Guild'
test_castle = 'a castle'
added_chat_ids = []
added_guild_tags = []
added_user_ids = []
added_user_guilds = []
added_user_chats = []


@session_handler
def add_guild(session: Session | None = None):
    global added_chat_ids, added_guild_tags, added_user_ids, added_user_guilds, added_user_chats
    new_guild = Guild(tag=test_guild_tag,
                      name=test_guild_name,
                      castle=test_castle)

    session.add(new_guild)
    session.commit()
    added_guild_tags.append(new_guild.tag)

    new_chat = Chat(id=1111,
                    group='allowed',
                    guild=test_guild_tag)
    session.add(new_chat)
    added_chat_ids.append(new_chat.id)
    new_other_chat = Chat(id=1212,
                          group='allowed',
                          alliance=1)
    session.add(new_other_chat)
    session.commit()
    added_chat_ids.append(new_other_chat.id)

    new_users = [
        User(id=i+1,
             username=f'user_{i+1}')
        for i in range(2)
    ]
    added_user_ids = list(map(lambda user: user.id, new_users))

    new_users_and_guilds = [
        UserAndGuild(user_id=i+1,
                     guild=test_guild_tag)
        for i in range(2)
    ]

    new_users_and_chats = [
        UserAndChat(user_id=i+1,
                    chat_id=1111)
        for i in range(2)
    ] + [
        UserAndChat(user_id=2,
                    chat_id=1212)
    ]  # let make some user a member of separated chat

    session.add_all([*new_users, *new_users_and_guilds, *new_users_and_chats])
    session.commit()
    added_user_guilds = list(
        map(lambda ug: (ug.user_id, ug.guild), new_users_and_guilds))
    added_user_chats = list(
        map(lambda uc: (uc.user_id, uc.chat_id), new_users_and_chats))


@session_handler
def delete_guild(session: Session | None = None):
    cur_guild = session.query(Guild).get(test_guild_tag)
    session.delete(cur_guild)


@session_handler
def delete_test_info(session: Session | None = None):
    session.delete(session.query(Chat).get(1212))
    user_ids = [1, 2]
    users = session.query(User) \
        .filter(User.id.in_(user_ids)).all()
    for user in users:
        session.delete(user)


@session_handler
def get_test_info(session: Session | None = None):
    user_entries_quant = session.query(func.count(User.id)).filter(
        User.id.in_(added_user_ids)).scalar()
    users_and_guilds_quant = session.query(func.count(UserAndGuild.user_id)) \
        .filter(UserAndGuild.user_id.in_(added_user_ids)).scalar()
    users_and_chats_quant = session.query(func.count(UserAndChat.user_id)) \
        .filter(UserAndChat.user_id.in_(added_user_ids)) \
        .filter(UserAndChat.chat_id.in_(added_chat_ids)).scalar()
    left_chat_ids = session.query(Chat.id) \
        .filter(Chat.id.in_(added_chat_ids)).all()
    return user_entries_quant, users_and_guilds_quant, users_and_chats_quant, left_chat_ids


class TestAddAndDeleteCapture(unittest.TestCase):
    def setUp(self) -> None:
        add_guild()

    def test_add(self):
        delete_guild()
        user_entries_quant, users_and_guilds_quant, users_and_chats_quant, left_chat_ids = get_test_info()
        self.assertEqual(user_entries_quant, len(added_user_ids))
        self.assertEqual(users_and_guilds_quant, 0)
        self.assertEqual(users_and_chats_quant, 1)
        left_chat_ids = sorted(map(lambda item: item[0], left_chat_ids))
        self.assertEquals(left_chat_ids, [1212])

    def tearDown(self) -> None:
        delete_test_info()


if __name__ == '__main__':
    unittest.main()
