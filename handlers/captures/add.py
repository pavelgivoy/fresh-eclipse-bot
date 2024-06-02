from aiogram import types
from aiogram.dispatcher.filters import Text
from database.models.chat import Chat

from loader import dp
from database.methods.captures import add_single
from database.methods.chat import get_group, get_locations_review_allowed
from filters.chat_filter import ChatFilter
from filters.forward_filter import ForwardFilter
from parsers.captures import parse_cw_capture_info, parse_ga_add_command
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import ADD_CAPTURE_ERROR_DEV, ADD_CAPTURE_ERROR_USER, KNOWN_CAPTURE, LOCATION_ADDED, NEW_CAPTURE, NOT_ENOUGH_CAPTURE_MANUAL_ADD_INFO, PROVIDE_ACTUAL_FORWARD
from utils.game_staff.captures_forward_text import CW_LOCATION_TEXT, CW_HEADQUARTER_TEXT
from utils.game_staff.ids import CW_BOT_ID


async def send_answer(message: types.Message,
                      chat: Chat | None,
                      name: str,
                      code: str,
                      result: str):
    group = get_group(chat)
    locations_review_allowed = get_locations_review_allowed(chat)

    if result == 'found' and locations_review_allowed and group in ['super', 'admin', 'allowed']:
        await message.answer(KNOWN_CAPTURE)
    elif result == 'added':
        await notify_admins(NEW_CAPTURE.format(name, code),
                            groups=['super', 'war', 'admin'])
        if locations_review_allowed and group in ['super', 'admin', 'allowed']:
            await message.answer(LOCATION_ADDED)
    else:
        await notify_admins(ADD_CAPTURE_ERROR_DEV)
        if locations_review_allowed and group in ['super', 'admin', 'allowed']:
            await message.answer(ADD_CAPTURE_ERROR_USER)


@dp.message_handler(commands=['ga_add'], chat_groups=['super', 'war', 'admin'])
async def process_manual_add(message: types.Message,
                             chat: Chat):
    code, name = parse_ga_add_command(message.get_args().split())

    if code is None or name is None:
        await message.answer(NOT_ENOUGH_CAPTURE_MANUAL_ADD_INFO)
        return

    result = add_single(code, name)
    await send_answer(message, chat, name, code, result)


@dp.message_handler(ForwardFilter(from_ids=[CW_BOT_ID], interval=24*60*60),
                    Text(contains=CW_LOCATION_TEXT) |
                    Text(contains=CW_HEADQUARTER_TEXT),
                    ChatFilter())
async def process_cw_forward_add(message: types.Message,
                                 chat: Chat):
    code, name = parse_cw_capture_info(message.text)
    result = add_single(code, name)
    await send_answer(message, chat, name, code, result)


# TODO handler for forwards from DDG bot


@dp.message_handler(Text(contains=CW_LOCATION_TEXT) |
                    Text(contains=CW_HEADQUARTER_TEXT))
async def process_deprecated_location_forward(message: types.Message):
    await message.answer(PROVIDE_ACTUAL_FORWARD.format('дня'))
