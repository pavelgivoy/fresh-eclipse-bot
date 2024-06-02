from email import message
import typing

from aiogram import types


def get_media(msg: types.Message) -> typing.Any | None:
    cur_instance = None
    media_type = None

    if msg.sticker:
        cur_instance = msg.sticker
        media_type = 'sticker'
    elif msg.animation:
        cur_instance = msg.animation
        media_type = 'animation'
    elif msg.voice:
        cur_instance = msg.voice
        media_type = 'voice'
    elif msg.video_note:
        cur_instance = msg.video_note
        media_type = 'video_note'
    # ! video and document are not the grouping types
    # ! an user can reply the certain video and document only
    # ! handlers also process the unique message only
    # ! though we see the coupled videos and documents, the messages are separated
    elif msg.video:
        cur_instance = msg.video
        media_type = 'video'
    elif msg.audio:
        cur_instance = msg.audio
        media_type = 'audio'
    elif msg.document:
        cur_instance = msg.document
        media_type = 'document'
    # ! photo is the unque grouping type
    # for this method we suppose to use the first photo (customer request)
    elif msg.photo:
        cur_instance = msg.photo[0]
        media_type = 'photo'

    return cur_instance, media_type
