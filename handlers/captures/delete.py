import re
from aiogram import types

from loader import dp
from utils.game_staff.answers import ALLIANCE_DEACTIVATED, ALLIANCE_UPDATE_STATUS_ERROR_DEV, ALLIANCE_UPDATE_STATUS_ERROR_USER, DELETE_LOCATION_ERROR_DEV, DELETE_LOCATION_ERROR_USER, LOCATION_DELETED, UNKNOWN_CAPTURE
from database.methods import captures
from utils.funcs.notify_admins import notify_admins


@dp.message_handler(regexp=r'^/(ga_delete)[_ ]([a-zA-Z0-9]{6}|unknown_\d{1,4})$', chat_groups=['super', 'war', 'admin'])
@dp.message_handler(regexp=r'^/(ga_forcedelete)[_ ]([a-zA-Z0-9]{6}|unknown_\d{1,4})$', chat_groups=['super'])
async def process_delete_capture(message: types.Message,
                                 regexp: re.Match):
    command = regexp.group(1)
    code = regexp.group(2)
    capture = captures.get_by_code(code)
    if capture is None:
        await message.answer(UNKNOWN_CAPTURE.format(code))
        return

    name = capture.name
    # capture must be deleted if it's instance of location or force deleting is used
    # alliances usually should be deactivated in case if they will play again later
    must_be_deleted = 'lvl.' in name or command == 'ga_forcedelete'
    res = captures.delete(capture, must_be_deleted)
    if res == 'deleted':
        await message.answer(LOCATION_DELETED.format(name, code))
    elif res == 'not deleted':
        await message.answer(ALLIANCE_DEACTIVATED.format(name))
    elif 'lvl.' in name:
        await notify_admins(DELETE_LOCATION_ERROR_DEV)
        await message.answer(DELETE_LOCATION_ERROR_USER)
    else:
        await notify_admins(ALLIANCE_UPDATE_STATUS_ERROR_DEV.format(name, code))
        await message.answer(ALLIANCE_UPDATE_STATUS_ERROR_USER)
