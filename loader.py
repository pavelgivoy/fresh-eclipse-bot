from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import filters

from utils.configs.bot_token import TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')
BOT_ID = bot.id
dp = Dispatcher(bot, storage=MemoryStorage())
filters.setup(dp)
