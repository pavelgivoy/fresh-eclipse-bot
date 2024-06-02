from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(commands=['cancel'], state='*')
async def reset_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return
    await state.finish()
    await message.answer('Обработка команды прервана')
