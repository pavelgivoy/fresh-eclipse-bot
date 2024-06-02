from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_pin_notify_keyboard():
    inline_btn_1 = InlineKeyboardButton(
        'Пин получен!', callback_data='got_pin')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    return inline_kb1
