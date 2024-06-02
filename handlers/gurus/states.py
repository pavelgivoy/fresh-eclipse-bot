from aiogram.dispatcher.filters.state import State, StatesGroup


class GuruUpdateStates(StatesGroup):
    WAIT_GURU_PROFILE = State()
    SET_GURU_USERNAME = State()
    SET_GURU_BS_LEVEL = State()
    SET_GURU_ALCH_LEVEL = State()
