from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.forward_filter import ForwardFilter
from keyboards.gurus.set_guru_level import set_guru_level_keyboard
from loader import dp
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import GUILD_IN_BASIC_ALLIANCE, GURU_UPDATE_ERROR_DEV, GURU_UPDATE_ERROR_USER, GURU_UPDATED, SELECT_GURU_SPEC_LEVEL, SEND_GURU_PROFILE, SEND_GURU_USERNAME
from utils.game_staff.basic_hq import BASIC_HQ_ID, BASIC_HQ_NAME
from utils.game_staff.castles import CASTLES_FROM_GURU_PROFILE
from utils.game_staff.ids import CW_BOT_ID

from database.methods import master, guild

from .states import GuruUpdateStates


@dp.message_handler(commands=['guru_update'], chat_groups=['super', 'war', 'admin'], chat_alliances=[BASIC_HQ_ID])
async def start_process_guru_update(message: types.Message):
    await GuruUpdateStates.WAIT_GURU_PROFILE.set()
    await message.answer(SEND_GURU_PROFILE)


@dp.message_handler(ForwardFilter(from_ids=[CW_BOT_ID]),
                    is_guru_profile=True,
                    state=GuruUpdateStates.WAIT_GURU_PROFILE,
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_parsed_guru_profile(message: types.Message,
                                      state: FSMContext,
                                      link: str,
                                      castle: str,
                                      guild_tag: str | None,
                                      alch_spec: str | None,
                                      bs_spec: str | None):
    found_guild = guild.get(guild_tag)
    if not found_guild:
        await message.answer(GUILD_IN_BASIC_ALLIANCE.format(guild_tag, 'не', BASIC_HQ_NAME))
        return
    await state.update_data(link=link,
                            castle=CASTLES_FROM_GURU_PROFILE[castle],
                            guild=guild_tag,
                            alch_spec=alch_spec,
                            bs_spec=bs_spec)
    await GuruUpdateStates.next()
    await message.answer(SEND_GURU_USERNAME)


@dp.message_handler(state=GuruUpdateStates.WAIT_GURU_PROFILE,
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_not_passed_guru_profile(message: types.Message):
    await message.answer(SEND_GURU_PROFILE)


@dp.message_handler(state=GuruUpdateStates.SET_GURU_USERNAME,
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_set_guru_username(message: types.Message,
                                    state: FSMContext):
    username = message.text.split('@')[-1]
    await state.update_data(username=username)
    data = await state.get_data()
    bs_spec = data.get('bs_spec')
    alch_spec = data.get('alch_spec')
    selected_spec = None
    if bs_spec:
        await GuruUpdateStates.SET_GURU_BS_LEVEL.set()
        selected_spec = bs_spec
        lvls = 6
    elif alch_spec:
        await GuruUpdateStates.SET_GURU_ALCH_LEVEL.set()
        selected_spec = alch_spec
        lvls = 7
    await message.answer(SELECT_GURU_SPEC_LEVEL.format(selected_spec), reply_markup=set_guru_level_keyboard(lvls))


async def process_update(callback_query: types.CallbackQuery, state: FSMContext, data: dict):
    update_res = master.update(link=data.get('link'),
                               castle=data.get('castle'),
                               username=data.get('username'),
                               guild=data.get('guild'),
                               alch_guru=data.get('alch_spec'),
                               alch_level=data.get('alch_level'),
                               bs_guru=data.get('bs_spec'),
                               bs_level=data.get('bs_level'))
    await state.finish()
    if update_res == 'updated':
        await callback_query.message.answer(GURU_UPDATED)
    else:
        await notify_admins(GURU_UPDATE_ERROR_DEV)
        await callback_query.message.answer(GURU_UPDATE_ERROR_USER)


@dp.callback_query_handler(lambda c: c.data.startswith('guru_level_'),
                           state=GuruUpdateStates.SET_GURU_ALCH_LEVEL,
                           chat_groups=['super', 'war', 'admin'],
                           chat_alliances=[BASIC_HQ_ID])
async def process_set_guru_alch_level(callback_query: types.CallbackQuery,
                                      state: FSMContext):
    alch_level = int(callback_query.data.split('guru_level_')[-1])
    await state.update_data(alch_level=alch_level)
    data = await state.get_data()
    bs_spec = data.get('bs_spec')
    if bs_spec:
        await GuruUpdateStates.next()
        await callback_query.message.answer(SELECT_GURU_SPEC_LEVEL.format(bs_spec), reply_markup=set_guru_level_keyboard(6))
    else:
        await process_update(callback_query, state, data)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data.startswith('guru_level_'),
                           state=GuruUpdateStates.SET_GURU_BS_LEVEL,
                           chat_groups=['super', 'war', 'admin'],
                           chat_alliances=[BASIC_HQ_ID])
async def process_set_guru_bs_level(callback_query: types.CallbackQuery,
                                    state: FSMContext):
    bs_level = int(callback_query.data.split('guru_level_')[-1])
    await state.update_data(bs_level=bs_level)
    data = await state.get_data()
    await process_update(callback_query, state, data)
    await callback_query.message.delete()
