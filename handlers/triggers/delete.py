from aiogram import types

from loader import dp
from database.methods import trigger
from utils.game_staff.answers import TRIGGER_DELETED, TRIGGER_EDIT_DENIED, TRIGGER_NAME_REQUIRED, TRIGGER_NOT_FOUND


async def process_delete_trigger(message: types.Message, is_global: bool):
    # search for trigger name
    trigger_name = message.get_args()
    if not trigger_name:
        await message.answer(TRIGGER_NAME_REQUIRED)
        return

    # search for trigger
    # global trigger
    chat_id = None
    found_trigger = trigger.get_by_name(trigger_name, chat_id)

    # global trigger can be deleted by devs only
    if found_trigger and not is_global:
        await message.answer(TRIGGER_EDIT_DENIED)
        return

    # local trigger
    if not found_trigger:
        chat_id = message.chat.id
        found_trigger = trigger.get_by_name(trigger_name, chat_id)

    if found_trigger:
        trigger.delete(found_trigger)
        await message.answer(TRIGGER_DELETED)
    else:
        await message.answer(TRIGGER_NOT_FOUND)


@dp.message_handler(commands=['delete_trigger'],
                    chat_groups=True,
                    user_groups=['super'])
async def process_delete_global_trigger(message: types.Message):
    await process_delete_trigger(message, is_global=True)


@dp.message_handler(commands=['delete_trigger'],
                    chat_groups=True)
async def process_delete_local_trigger(message: types.Message):
    await process_delete_trigger(message, is_global=False)
