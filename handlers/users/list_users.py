from aiogram import types

from loader import dp
from database.methods import user_and_guild, user_and_chat
from parsers.users import parse_user_and_chat, parse_list_users_and_guilds_command


@dp.message_handler(commands=['list_users_and_chats'],
                    chat_groups=['super'])
async def process_list_users_and_chats(message: types.Message):
    chat_id, user_id = parse_user_and_chat(message.get_args().split())
    users_and_chats = user_and_chat.get_all(user_id=user_id, chat_id=chat_id)
    ans = '[' + ',\n'.join(list(map(str, users_and_chats))) + ']'
    await message.answer(ans)


@dp.message_handler(commands=['list_users_and_guilds'],
                    chat_groups=['super'])
async def process_list_users_and_guilds(message: types.Message):
    user_id, guild_tag = parse_list_users_and_guilds_command(
        message.get_args().split())
    users_and_guilds = user_and_guild.get_all(
        user_id=user_id, guild=guild_tag)
    ans = '[' + ',\n'.join(list(map(str, users_and_guilds))) + ']'
    await message.answer(ans)
