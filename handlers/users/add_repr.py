from aiogram import types

from loader import dp
from database.methods.user_and_guild import add_repr
from parsers.users import parse_add_repr_command
from utils.game_staff.answers import ADD_REPR_DONE, ADD_REPR_ERROR_DEV, GUILD_IN_BASIC_ALLIANCE, USER_INFO_REQUIRED, USER_IS_REPR
from utils.game_staff.basic_hq import BASIC_HQ_NAME


@dp.message_handler(commands=['add_repr'],
                    chat_groups=['super'])
async def process_add_repr(message: types.Message):
    args = message.get_args().split()
    guild_tag, user_id, username = parse_add_repr_command(args)
    if not guild_tag or not username:
        await message.answer(USER_INFO_REQUIRED)
        return

    update_res = add_repr(guild_tag, user_id, username)
    if update_res == 'guild_not_found':
        await message.answer(GUILD_IN_BASIC_ALLIANCE.format(guild_tag, 'не', BASIC_HQ_NAME))
    elif update_res == 'repr_found':
        await message.answer(USER_IS_REPR.format(username, guild_tag))
    elif update_res == 'error':
        await message.answer(ADD_REPR_ERROR_DEV)
    else:
        await message.answer(ADD_REPR_DONE.format(guild_tag, username))
