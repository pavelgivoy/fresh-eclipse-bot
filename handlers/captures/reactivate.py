import re

from aiogram import types

from loader import dp
from utils.game_staff.answers import ALLIANCE_ACTIVE, ALLIANCE_UPDATE_STATUS_ERROR_DEV, ALLIANCE_UPDATE_STATUS_ERROR_USER, UNKNOWN_CAPTURE
from database.methods import captures
from utils.funcs.notify_admins import notify_admins


@dp.message_handler(regexp=r'^/ga_reactivate[_ ]([a-zA-Z0-9]{6}|unknown_\d{1,4})$', chat_groups=['super', 'war'])
async def process_reactivate_alliance(message: types.Message,
                                      regexp: re.Match):
    code = regexp.group(1)

    alliance = captures.get_by_code(code)
    if alliance is None:
        await message.answer(UNKNOWN_CAPTURE.format(code))
        return
    name = alliance.name

    res = 'not deleted'
    if not alliance.active:
        res = captures.delete(alliance, must_be_deleted=False)
    if res == 'not deleted':
        await message.answer(ALLIANCE_ACTIVE.format(name))
    else:
        await notify_admins(ALLIANCE_UPDATE_STATUS_ERROR_DEV.format(name, code))
        await message.answer(ALLIANCE_UPDATE_STATUS_ERROR_USER)
