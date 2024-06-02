from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def set_guru_level_keyboard(levels: int) -> InlineKeyboardMarkup:
    row_width = 3
    markup = InlineKeyboardMarkup(row_width=row_width)

    for i in range(levels):
        if i % row_width == 0:
            markup.row()
        btn = InlineKeyboardButton(f'{i+1}', callback_data=f'guru_level_{i+1}')
        markup.insert(btn)

    return markup
