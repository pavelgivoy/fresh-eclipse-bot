from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(commands=['get_state'], state='*', user_groups=['super'])
async def get_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    await message.answer(current_state)
