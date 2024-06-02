from aiogram import types

from loader import dp
from database.methods.captures import get_by_code
from database.methods.resources import get_all, delete, update
from parsers.resources import parse_new_resource_info
from utils.game_staff.answers import DELETE_RESOURCE_INFO_DONE, DELETE_RESOURCE_INFO_ERROR_DEV, DELETE_RESOURCE_INFO_ERROR_USER, UNKNOWN_BUFF_TYPE_OR_PRICE, UPDATE_RESOURCE_INFO_DONE, UPDATE_RESOURCE_INFO_ERROR_DEV, UPDATE_RESOURCE_INFO_ERROR_USER
from utils.game_staff.resources import RESOURCES, RESOURCE_STAFF
from utils.funcs.notify_admins import notify_admins


def modify_row_buttons(callback_query: types.CallbackQuery,
                       keyboard: list[types.InlineKeyboardButton],
                       save_mark: bool):
    """Modify message markup in the row

    :param types.CallbackQuery callback_query: callback query
    :param list[types.InlineKeyboardButton] keyboard: keyboard buttons list which should be changed
    :param bool save_mark: True if previous mark should be saved, else False
    """
    for i in range(len(keyboard)):
        if '✅' in keyboard[i].text and (not save_mark or keyboard[i].callback_data == callback_query.data):
            keyboard[i].text = keyboard[i].text.replace('✅', '')
        elif '✅' not in keyboard[i].text and keyboard[i].callback_data == callback_query.data:
            keyboard[i].text = '✅' + keyboard[i].text


@dp.callback_query_handler(lambda c: any([any([c.data.startswith(str(elem)) for elem in list_elem]) for list_elem in RESOURCE_STAFF]),
                           chat_groups=['super', 'war', 'admin'])
async def accept_choice(callback_query: types.CallbackQuery):
    c_data = callback_query.data
    markup = callback_query.message.reply_markup
    keyboard = markup.inline_keyboard
    required_row = 0
    for i in range(len(keyboard)):
        for j in range(len(keyboard[i])):
            if keyboard[i][j].callback_data == c_data:
                required_row = i
                break
    modify_row_buttons(callback_query,
                       keyboard[required_row],
                       any([c_data.startswith(elem) for elem in RESOURCES]))
    await callback_query.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('update_loc_info_'),
                           chat_groups=['super', 'war', 'admin'])
async def update_location_info(callback_query: types.CallbackQuery):
    code = callback_query.data.split('update_loc_info_')[-1]

    markup = callback_query.message.reply_markup
    keyboard = markup.inline_keyboard

    resources, buff, price = parse_new_resource_info(keyboard)

    location = get_by_code(code)
    if (buff and not price) or (not buff and price):
        await callback_query.answer(UNKNOWN_BUFF_TYPE_OR_PRICE.format(location.name), show_alert=True)

    update_res = update(location, resources, buff, price)
    if update_res == 'error':
        await notify_admins(UPDATE_RESOURCE_INFO_ERROR_DEV.format(location.name))
        await callback_query.answer(UPDATE_RESOURCE_INFO_ERROR_USER.format(location.name), show_alert=True)
    else:
        await callback_query.answer(UPDATE_RESOURCE_INFO_DONE)


@dp.callback_query_handler(lambda c: c.data.startswith('delete_loc_info_'),
                           chat_groups=['super', 'war', 'admin'])
async def delete_buff_and_resources_info(callback_query: types.CallbackQuery):
    code = callback_query.data.split('delete_loc_info_')[-1]
    location = get_by_code(code)
    resources = get_all(location_ids=[location.id])
    delete_res = delete(resources)
    if delete_res == 'error':
        await notify_admins(DELETE_RESOURCE_INFO_ERROR_DEV.format(location.name))
        await callback_query.answer(DELETE_RESOURCE_INFO_ERROR_USER, show_alert=True)
    else:
        await callback_query.answer(DELETE_RESOURCE_INFO_DONE)
