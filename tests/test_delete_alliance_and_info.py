import unittest

from sqlalchemy import func
from sqlalchemy.orm.session import Session

from database.methods import captures, guild, user, chat
from database.methods.common import session_handler
from database.models.alliance import Alliance
from database.models.chat import Chat
from database.models.db_conn import DatabaseConnection
from database.models.guild import Guild
from database.models.user import User
from database.models.user_and_guild import UserAndGuild
from database.models.user_and_chat import UserAndChat


alliance_id = 4
other_alliance_id = 5
guild_tags = [f'TS{chr(i)}'.upper()
              for i in range(97, 102)]  # 97 -> A; 101 -> E
guild_names = [f'Test Guild {chr(i)}' for i in range(97, 102)]
castle = "a castle"
guilds_quant = 0
users_quant = 0
chats_quant = 0
users_and_guilds_quant = 0
users_and_chats_qunat = 0
user_ids = []
chat_ids = []


def add_test_info():
    global guilds_quant, chats_quant, users_quant, users_and_chats_quant, users_and_guilds_quant, user_ids, chat_ids
    with DatabaseConnection() as session:
        # add alliances
        alliance_name = 'Some Alliance'
        alliance_code = 'random'
        alliance_owner = 'TSA'
        alliance = Alliance(id=alliance_id,
                            name=alliance_name,
                            code=alliance_code,
                            owner=alliance_owner)
        session.add(alliance)

        other_alliance_name = 'Other alliance'
        other_alliance_code = 'other1'
        other_alliance_owner = 'TST'
        other_alliance = Alliance(id=other_alliance_id,
                                  name=other_alliance_name,
                                  code=other_alliance_code,
                                  owner=other_alliance_owner)
        session.add(other_alliance)

        # add guilds
        guilds = [
            Guild(tag=guild_tags[i],
                  name=guild_names[i],
                  castle=castle,
                  alliance=alliance_id)
            for i in range(len(guild_tags))
        ]
        guilds.append(Guild(tag='TST',
                            name='Test Guild T',
                            castle=castle,
                            alliance=other_alliance_id))
        session.add_all(guilds)
        session.commit()
        guilds_quant = len(guilds)

        # add chats
        # guild chats
        chats = [
            Chat(id=123123123+i,
                 group='allowed',
                 guild=guild_tags[i],
                 alliance=alliance_id)
            for i in range(len(guild_tags))
        ]
        # alliance admin chat
        chats.append(Chat(id=123123123+len(guild_tags),
                          group='admin',
                          alliance=alliance_id))
        # other alliance guild and admin chats
        chats.extend([
            Chat(id=1234,
                 group='allowed',
                 guild='TST',
                 alliance=other_alliance_id),
            Chat(id=1235,
                 group='admin',
                 alliance=other_alliance_id)
        ])
        session.add_all(chats)
        chat_ids = list(map(lambda chat: chat.id, chats))
        chats_quant = len(chats)

        # add users
        users = [
            User(id=i+1,
                 username=f'user_{i+1}',)
            for i in range(len(guild_tags))
        ]
        user_ids = list(map(lambda user: user.id, users))
        session.add_all(users)
        session.commit()
        users_quant = len(users)

        # add matches with guilds and chats
        users_and_guilds = [
            UserAndGuild(user_id=i+1,
                         guild=guild_tags[i])
            for i in range(len(guild_tags))
        ]
        users_and_chats = [
            UserAndChat(user_id=i+1,
                        chat_id=123123123+i)
            for i in range(len(guild_tags))
        ]
        # let make some users members of other alliance
        users_and_guilds.append(
            UserAndGuild(user_id=1,
                         guild='TST')
        )
        users_and_chats.extend([
            UserAndChat(user_id=1,
                        chat_id=1234),
            UserAndChat(user_id=1,
                        chat_id=1235)
        ])
        session.add_all(users_and_guilds)
        session.add_all(users_and_chats)
        session.commit()
        users_and_guilds_quant = len(users_and_guilds)
        users_and_chats_quant = len(users_and_chats)


@session_handler
def delete_test_info(session: Session | None = None):
    captures.delete(captures.get(other_alliance_id),
                    True,
                    session=session)
    user_ids = list(range(1, len(guild_tags)+1))
    user.delete(user.get_all(user_ids=user_ids,
                session=session), session=session)
    guild.delete(guild.get_all(tags=guild_tags +
                 ['TST'], session=session), session=session)
    chat_ids = [123123123+i for i in range(len(guild_tags))] + [1234, 1235]
    chat.delete(chat.get_all(chat_ids=chat_ids,
                session=session), session=session)


@session_handler
def get_test_info(session: Session | None = None):
    user_entries_quant = session.query(func.count(User.id)).filter(
        User.id.in_(user_ids)).scalar()
    users_and_guilds_quant = session.query(func.count(UserAndGuild.user_id)) \
        .filter(UserAndGuild.user_id.in_(user_ids)).scalar()
    users_and_chats_quant = session.query(func.count(UserAndChat.user_id)) \
        .filter(UserAndChat.user_id.in_(user_ids)) \
        .filter(UserAndChat.chat_id.in_(chat_ids)).scalar()
    left_chat_ids = session.query(Chat.id) \
        .filter(Chat.id.in_(chat_ids)).all()
    added_guilds = guild_tags[:]
    added_guilds.append('TST')
    left_guilds = session.query(Guild.tag) \
        .filter(Guild.tag.in_(added_guilds)).all()
    return user_entries_quant, users_and_guilds_quant, users_and_chats_quant, left_chat_ids, left_guilds


class TestDeleteAllianceInfo(unittest.TestCase):
    def setUp(self) -> None:
        add_test_info()

    def test_delete_alliance_info(self):
        captures.delete(captures.get(alliance_id),
                        True)
        user_entries_quant, users_and_guilds_entries_quant, users_chats_entries_quant, left_chat_ids, left_guilds = get_test_info()
        self.assertEqual(user_entries_quant, users_quant)
        self.assertEqual(users_and_guilds_entries_quant,
                         users_and_guilds_quant)
        self.assertEquals(left_chat_ids, [(1234,), (1235,)])
        self.assertEqual(len(left_guilds), guilds_quant)
        self.assertEqual(users_chats_entries_quant,
                         len([(1234,), (1235,)]))

    def tearDown(self) -> None:
        delete_test_info()


if __name__ == '__main__':
    unittest.main()
