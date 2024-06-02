import logging

from aiogram import executor, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from utils.configs.logs_file import LOGS_FILE


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning("Bot down")


if __name__ == '__main__':
    from handlers import dp

    logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.DEBUG, filename=LOGS_FILE)

    dp.middleware.setup(LoggingMiddleware())

    executor.start_polling(dp,
                           allowed_updates=types.AllowedUpdates.all(),
                           skip_updates=True,
                           on_shutdown=on_shutdown)
