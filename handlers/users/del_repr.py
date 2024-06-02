from aiogram import types

from database.methods.user_and_guild import delete_repr
from loader import dp
from parsers.users import parse_del_repr_command
from utils.game_staff.answers import DELETE_REPR_DONE, DELETE_REPR_ERROR_DEV, ERROR_HAPPENED_USER, GUILD_IN_BASIC_ALLIANCE, UNKNOWN_FLAG_WARNING, USER_INFO_REQUIRED, USER_IS_NOT_REPR
from utils.game_staff.basic_hq import BASIC_HQ_NAME


@dp.message_handler(commands=['del_repr'],
                    chat_groups=['super'])
async def process_delete_repr(message: types.Message):
    args = message.get_args().split()
    guild_tag, user_info, flag = parse_del_repr_command(args)
    if not guild_tag or not user_info:
        await message.answer(USER_INFO_REQUIRED)
        return
    if flag != 'force' and flag is not None:
        await message.answer(UNKNOWN_FLAG_WARNING.format(flag))

    update_res = delete_repr(guild_tag, user_info, flag)
    if update_res == 'guild_not_found':
        await message.answer(GUILD_IN_BASIC_ALLIANCE.format(guild_tag, 'не', BASIC_HQ_NAME))
    elif update_res == 'repr_not_found':
        repr_user_info = 'с айди' if user_info is int else 'с юзернеймом'
        await message.answer(USER_IS_NOT_REPR.format(repr_user_info, user_info, guild_tag))
    elif update_res == 'error':
        await message.answer(DELETE_REPR_ERROR_DEV.format(guild_tag))
    elif update_res == 'deleted':
        repr_user_info = 'с айди' if user_info is int else 'с юзернеймом'
        await message.answer(DELETE_REPR_DONE.format(repr_user_info, user_info, guild_tag))
    else:
        await message.answer(ERROR_HAPPENED_USER)
