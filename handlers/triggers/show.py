from re import M
from aiogram import types

from loader import dp
from database.methods import trigger


@dp.message_handler(commands=['triggerlist'],
                    chat_groups=True)
async def process_show_triggers(message: types.Message):
    global_chat_id = None
    local_chat_id = message.chat.id
    triggers = trigger.get_all(chat_ids=[global_chat_id,
                                         local_chat_id])

    ttt = {  # trigger type translations
        'text': 'текст',
        'sticker': 'стикер',
        'animation': 'GIF',
        'voice': 'войс',
        'video_note': 'кружок',
        'video': 'видео',
        'audio': 'аудио',
        'document': 'документ',
        'photo': 'фото',
    }

    glob_ans = '<b>Глобальные:</b>\n'
    loc_ans = '<b>Локальные:</b>\n'
    for tr in triggers:
        strict_type = 'строгий' if tr.strict else 'нестрогий'
        ans_pattern = f'\n{tr.name}: <code>{ttt[tr.type]}</code> <i>{strict_type}</i>'
        if tr.chat_id is None:
            glob_ans += ans_pattern
        elif tr.chat_id == local_chat_id:
            loc_ans += ans_pattern

    await message.answer(glob_ans + '\n\n' + loc_ans)
