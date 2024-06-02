from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def loc_info_keyboard(buttons: list[list[str | int]], code: str):
    inline_kb = InlineKeyboardMarkup(row_width=max(
        [len(button_list) for button_list in buttons]))
    for button_list in buttons:
        inline_kb.row()
        for button_elem in button_list:
            inline_btn = InlineKeyboardButton(button_elem,
                                              callback_data=f'{button_elem}_{code}')
            inline_kb.insert(inline_btn)
    inline_kb.add(InlineKeyboardButton(
        'Обновить', callback_data=f'update_loc_info_{code}'))
    inline_kb.add(InlineKeyboardButton('Удалить информацию о бафах и ресурсах',
                                       callback_data=f'delete_loc_info_{code}'))
    return inline_kb
