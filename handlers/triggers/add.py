from aiogram import types

from loader import dp
from database.methods import trigger
from utils.funcs.get_media import get_media
from utils.game_staff.answers import TRIGGER_ADDED, TRIGGER_EDIT_DENIED, TRIGGER_NAME_REQUIRED, TRIGGER_PARSE_FAILED


async def process_add_trigger(message: types.Message, is_global: bool):
    # search for trigger name
    # ! get_args() doesn't work with an exclamation mark
    trigger_name = message.text.split('trigger')[-1].strip()
    if not trigger_name:
        await message.answer(TRIGGER_NAME_REQUIRED)
        return

    # search for trigger
    # global trigger
    chat_id = None
    found_trigger = trigger.get_by_name(trigger_name, chat_id)

    # global trigger cannot be edited through local trigger command
    if found_trigger and not is_global:
        await message.answer(TRIGGER_EDIT_DENIED)
        return

    # parse replied message (trigger body)
    msg = message.reply_to_message
    text = msg.text or msg.caption
    media_instance, trigger_type = get_media(msg)
    # any of text or media instance should be found to add trigger
    if not text and not media_instance:
        await message.answer(TRIGGER_PARSE_FAILED)
        return

    if not trigger_type and text:
        trigger_type = 'text'

    file_id = media_instance.file_id if media_instance else None
    strict = message.text.startswith('/')

    if not is_global:
        chat_id = message.chat.id
        found_trigger = trigger.get_by_name(trigger_name, chat_id)

    if found_trigger:
        trigger.edit(trigger=found_trigger,
                     trigger_type=trigger_type,
                     message_id=msg.message_id,
                     text_value=text,
                     file_id=file_id,
                     strict=strict)
    else:
        trigger.add(trigger_type=trigger_type,
                    chat_id=chat_id,
                    message_id=msg.message_id,
                    name=trigger_name,
                    text_value=text,
                    file_id=file_id,
                    strict=strict)
    await message.answer(TRIGGER_ADDED)


@dp.message_handler(commands=['global_trigger'],
                    commands_prefix='!/',
                    is_reply=True,
                    chat_groups=True,
                    user_groups=['super'])
async def process_add_global_trigger(message: types.Message):
    await process_add_trigger(message, is_global=True)


@dp.message_handler(commands=['trigger'],
                    commands_prefix='!/',
                    is_reply=True,
                    chat_groups=True,
                    user_groups=True,
                    user_is_admin=True)
async def process_add_local_trigger(message: types.Message):
    await process_add_trigger(message, is_global=False)
