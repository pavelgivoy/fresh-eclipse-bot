from pydoc import doc
from aiogram import types

from loader import dp
from filters.chat_filter import ChatFilter
from filters.trigger_filter import TriggerFilter


@dp.message_handler(ChatFilter(chat_groups=True,
                               triggers_allowed=True),
                    TriggerFilter())
async def process_answer_trigger(message: types.Message,
                                 text: str | None = None,
                                 photo: types.InputMediaPhoto | None = None,
                                 video: types.InputMediaVideo | None = None,
                                 audio: types.InputMediaAudio | None = None,
                                 voice: types.Voice | None = None,
                                 video_note: types.VideoNote | None = None,
                                 sticker: types.Sticker | None = None,
                                 animation: types.Animation | None = None,
                                 document: types.Document | None = None
                                 ):
    if photo:
        await message.answer_photo(photo=photo, caption=text)
    elif video:
        await message.answer_video(video=video, caption=text)
    elif audio:
        await message.answer_audio(audio=audio, caption=text)
    elif voice:
        await message.answer_voice(voice=voice, caption=text)
    elif video_note:
        await message.answer_video_note(video_note=video_note)
    elif sticker:
        await message.answer_sticker(sticker=sticker)
    elif animation:
        await message.answer_animation(animation=animation, caption=text)
    elif document:
        await message.answer_document(document=document, caption=text)
    else:
        await message.answer(text=text)
