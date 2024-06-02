import re

from aiogram import types

from database.methods.guild import get
from loader import dp
from utils.game_staff.regexps import GUILD_TAG


@dp.message_handler(commands=['guild_info'],
                    chat_groups=['super'])
async def process_guild_info(message: types.Message):
    found_guild_tag = re.match(GUILD_TAG, message.get_args())
    if not found_guild_tag:
        await message.answer('Про какую гильдию вы хотите узнать?')
        return
    await message.answer(str(get(found_guild_tag.group(0))))
