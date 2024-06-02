from aiogram import types
from aiogram.dispatcher.filters.builtin import ChatTypeFilter
from database.models.chat import Chat

from loader import dp
from database.methods.chat import get_chat_from_group_chat_id, edit
from filters.chat_filter import ChatFilter
from filters.user_is_admin_of_input_chat import UserIsAdminOfInputChat
from keyboards.chats.edit_chat_info import edit_chat_info_keyboard
from parsers.chats import parse_chat_id_info
from utils.funcs.notify_admins import notify_admins
from utils.funcs.remove_markdowns import remove_markdowns
from utils.game_staff.answers import CHAT_ID_INPUT_IS_NOT_ALLOWED, CHAT_SETTING_CHANGING_ERROR_USER, CHAT_SETTINGS_CHANGED, CHAT_SETTINGS_CHANGING_ERROR_DEV, CHAT_UNKNOWN
from utils.game_staff.chatset_translating import status_from_bool, status_from_key


@dp.message_handler(commands=['edit_chat'],
                    user_is_admin=True,
                    chat_groups=True)
async def process_edit_chat_command_for_other_users(message: types.Message, chat: Chat | None):
    change_group_allowed = chat and chat.group == 'super'

    chat_id = parse_chat_id_info(message)
    if not change_group_allowed and chat_id:
        await message.answer(CHAT_ID_INPUT_IS_NOT_ALLOWED)
        chat_id = None

    if chat_id:
        chat = get_chat_from_group_chat_id(chat_id)
    if not chat:
        await message.answer(CHAT_UNKNOWN.format(chat_id))
        return

    ans = f'chat id: {chat.id}\n'
    if change_group_allowed:
        ans += f'group: {chat.group}\n'
    markup, chatset_data = edit_chat_info_keyboard(chat, change_group_allowed)
    ans += chatset_data
    await message.answer(ans, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('chatset_option'),
                           user_is_admin=True,
                           chat_groups=True)
async def on_chatset_option_button_click(callback_query: types.CallbackQuery):
    row_num = int(callback_query.data.split()[-1])

    markup = callback_query.message.reply_markup
    old_button_text = markup.inline_keyboard[row_num][0].text
    old_status = old_button_text.split(': ')[-1]
    old_status = status_from_key[old_status]
    new_status = status_from_bool[not old_status]
    old_status = status_from_bool[old_status]
    new_button_text = old_button_text.replace(old_status, new_status)
    cur_message_text = callback_query.message.text
    msg = cur_message_text.replace(old_button_text, new_button_text)
    markup.inline_keyboard[row_num][0].text = new_button_text
    await callback_query.message.edit_text(msg, reply_markup=markup)
    await callback_query.answer('OK')


@dp.callback_query_handler(lambda c: 'group' in c.data, chat_groups=['super'])
async def on_group_button_click(callback_query: types.CallbackQuery):
    row_num, col_num = callback_query.data.split()[-1].split('_')
    row_num, col_num = int(row_num), int(col_num)

    message = callback_query.message
    message_text = message.text
    markup = message.reply_markup

    for i in range(len(markup.inline_keyboard[row_num])):
        button = markup.inline_keyboard[row_num][i]
        button_text = button.text
        if '✅' in button_text and i == col_num:  # don't execute a duplicated job
            break
        elif '✅' in button_text:
            button.text = button.text.replace('✅', '')
        elif i == col_num:
            button.text = '✅' + button_text
            group = message_text.split('group: ')[-1].split('\n')[0]
            message_text = message_text.replace(group, button_text)

    await message.edit_text(message_text, reply_markup=markup)
    await callback_query.answer('OK')


@dp.callback_query_handler(lambda c: c.data == 'apply_chatset_changes',
                           user_is_admin=True,
                           chat_groups=True)
async def on_apply_chatset_changes_button_click(callback_query: types.CallbackQuery, chat: Chat | None):
    message = callback_query.message
    text = message.text
    chat_id = text.split('chat id: ')[-1].split('\n')[0]
    input_chat = get_chat_from_group_chat_id(int(chat_id))
    if not input_chat:
        await callback_query.answer(remove_markdowns(CHAT_UNKNOWN.format(chat_id)), show_alert=True)
        return

    if chat.group == 'super':
        group = text.split('group: ')[-1].split('\n')[0]
        input_chat.group = group

    res = edit(input_chat, text.split('\n'))

    if res == 'edited':
        await callback_query.answer(remove_markdowns(CHAT_SETTINGS_CHANGED.format(chat_id)),
                                    show_alert=True)
    else:
        await notify_admins(CHAT_SETTINGS_CHANGING_ERROR_DEV.format(chat_id))
        await callback_query.answer(CHAT_SETTING_CHANGING_ERROR_USER,
                                    show_alert=True)
