from aiogram import types

from loader import dp
from database.methods.history import update_location_owner
from parsers.captures import parse_force_update_location_owner_command
from utils.funcs.get_battle_time import get_previous_battle_time
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import FORCE_UPDATE_OWNER_DONE, FORCE_UPDATE_OWNER_ERROR_DEV, FORCE_UPDATE_OWNER_ERROR_USER, FORCE_UPDATE_OWNER_WRONG_ARGS, HISTORY_NOT_FOUND, LOCATION_IS_OWNER_FORBIDDEN, UNKNOWN_CAPTURE, UNKNOWN_OWNER


@dp.message_handler(commands=['force_update_location_owner'], chat_groups=['super', 'war'])
async def force_update_location_owner(message: types.Message):
    arg_list = message.get_args().split()
    code, new_owner = parse_force_update_location_owner_command(arg_list)
    if not code or not new_owner:
        await message.answer(FORCE_UPDATE_OWNER_WRONG_ARGS)
        return
    if 'lvl.' in new_owner:
        await message.answer(LOCATION_IS_OWNER_FORBIDDEN)
        return
    battle_date = get_previous_battle_time(message.date)

    update_res = update_location_owner(code, battle_date, new_owner)
    if update_res == 'capture_not_found':
        await message.answer(UNKNOWN_CAPTURE.format(code))
    elif update_res == 'history_not_found':
        await message.answer(HISTORY_NOT_FOUND)
    elif update_res == 'owner_not_found':
        await message.answer(UNKNOWN_OWNER.format(new_owner))
    elif update_res == 'updated':
        await message.answer(FORCE_UPDATE_OWNER_DONE)
    else:
        await notify_admins(FORCE_UPDATE_OWNER_ERROR_DEV)
        await message.answer(FORCE_UPDATE_OWNER_ERROR_USER)
