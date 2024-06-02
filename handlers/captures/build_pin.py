from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from ...filters.chat_filter import ChatFilter


@dp.message_handler(ChatFilter(groups=['super', 'war']),
                    commands=['build_pin'])
async def build_pin(message: types.Message):
    # TODO
    pass
