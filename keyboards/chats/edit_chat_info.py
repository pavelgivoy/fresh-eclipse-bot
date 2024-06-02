from aiogram import types

from database.models.chat import Chat

from utils.game_staff.chatset_translating import settings_translating, status_from_bool


def edit_chat_info_keyboard(chat: Chat, change_group_allowed: bool):
    markup = types.InlineKeyboardMarkup(row_width=5)

    row_num = 0
    if change_group_allowed:
        markup.row()
        groups = ['super', 'war', 'admin', 'allowed', 'not_allowed']
        for i in range(len(groups)):
            is_current = '✅' if chat.group == groups[i] else ''
            text = f'{is_current}{groups[i]}'
            callback_data = f'{groups[i]}_group {row_num}_{i}'
            button = types.InlineKeyboardButton(text=text,
                                                callback_data=callback_data)
            markup.insert(button)
        row_num += 1

    chatset_data = ''  # collects button texts to reuse them in message
    for k, v in settings_translating.items():
        markup.row()
        status = status_from_bool[bool(chat.__getattribute__(k))]
        text = f'{v}: {status}'
        chatset_data += text + '\n'
        callback_data = f'chatset_option {row_num}'
        button = types.InlineKeyboardButton(text=text,
                                            callback_data=callback_data)
        markup.add(button)
        row_num += 1

    apply_changes_kb = types.InlineKeyboardButton('Применить изменения',
                                                  callback_data='apply_chatset_changes')
    markup.add(apply_changes_kb)

    return markup, chatset_data
