from aiogram import types

from database.methods import user_and_chat
from database.models.user import User
from loader import dp
from database.methods import user
from database.methods.user_and_chat import add_user
from parsers.users import parse_user_and_chat
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import ADD_USER_AND_CHAT_DONE, ADD_USER_AND_CHAT_ERROR_DEV, ADD_USER_AND_CHAT_ERROR_USER, ADD_USER_ERROR_DEV, USER_ID_REQUIRED, USER_MEMBER_INFO_UPDATE_FAILED


async def add_user_and_chat(message: types.Message,
                            user_id: int,
                            chat_id: int):
    # get chat member instance to know user privelleges
    found_user_in_chat = await message.bot.get_chat_member(chat_id, user_id)
    # an user is not a member of the given chat
    if found_user_in_chat.status == 'left':
        await message.answer(USER_MEMBER_INFO_UPDATE_FAILED)
        return

    # check user and chat entry appearance to avoid unique constraint violation
    found_db_user_and_chat = user_and_chat.get(user_id, chat_id)
    if found_db_user_and_chat and found_db_user_and_chat.is_admin == found_user_in_chat.is_chat_admin():
        await message.answer(ADD_USER_AND_CHAT_DONE)
        return

    # check if the user exists in the database
    # if not, create the user instance
    found_db_user = user.get(user_id)
    if not found_db_user:
        update_res = user.update([User(id=user_id,
                                       username=found_user_in_chat.user.username)])
        if update_res == 'error':
            await notify_admins(ADD_USER_ERROR_DEV.format(user_id))
            await message.answer(ADD_USER_AND_CHAT_ERROR_USER)
            return

    update_res = add_user(user_id=user_id,
                          chat_id=chat_id,
                          is_admin=found_user_in_chat.is_chat_admin())
    if update_res == 'error':
        await notify_admins(ADD_USER_AND_CHAT_ERROR_DEV.format(chat_id))
        await message.answer(ADD_USER_AND_CHAT_ERROR_USER)
    else:
        await message.answer(ADD_USER_AND_CHAT_DONE)


@dp.message_handler(commands=['add_user_and_chat'],
                    user_groups=['super'])
async def process_add_user_and_chat(message: types.Message):
    args = message.get_args().split()
    chat_id, user_id = parse_user_and_chat(args)
    if not user_id:
        await message.answer(USER_ID_REQUIRED)
        return
    if not chat_id:
        chat_id = message.chat.id

    await add_user_and_chat(message, user_id, chat_id)


@dp.message_handler(commands=['remind_me'],
                    chat_groups=True)
async def process_add_user_and_chat_from_user(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    await add_user_and_chat(message, user_id, chat_id)
