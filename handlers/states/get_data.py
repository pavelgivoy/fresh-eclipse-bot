from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(commands=['get_state_data'], state='*', user_groups=['super'])
async def get_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.answer(str(await state.get_data()))
