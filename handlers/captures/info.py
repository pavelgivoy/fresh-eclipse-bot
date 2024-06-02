import re

from aiogram import types

from loader import dp
from database.methods.captures import get_by_code
from database.methods.resources import get_capture_info
from keyboards.captures.loc_info import loc_info_keyboard
from utils.game_staff.answers import UNKNOWN_CAPTURE
from utils.game_staff.resources import RESOURCES, MINE_BUFFS, MINE_PRICES, GP_BUFFS, GP_PRICES


@dp.message_handler(regexp=r'^/i[_ ]([a-zA-Z0-9]{6}|unknown_\d{1,4})$',
                    chat_groups=['super', 'war', 'admin'])
async def process_info_command(message: types.Message,
                               regexp: re.Match):
    code = regexp.group(1)
    capture = get_by_code(code)
    if not capture:
        await message.answer(UNKNOWN_CAPTURE.format(code))
        return

    capture_info = get_capture_info(capture)
    name = capture_info['name']
    owner = capture_info['owner']

    ans = f'<b>{name}</b> <code>{code}</code>\n\n'
    ans += f'Владелец: {owner}\n'

    markup = None

    if 'lvl.' in name:  # => instance of Location
        ans += f'Прожито битв: {capture_info["life_time"]}\n'
        ans += f'Прожито битв под контролем у нынешнего владельца: {capture_info["owned_time"]}\n'
        resources_str = ", ".join(map(lambda resource: resource.name,
                                      capture_info["resources"])) or "неизвестно"
        ans += f'Дроп: {resources_str}\n'
        # ruins cannot have buffs, other locations do
        no_buffs_ans = "" if "Ruins" in name else "неизвестно"
        buffs_str = "; ".join(map(lambda buff: buff.name + " за " +
                                  str(buff.price) + "🎖", capture_info["buffs"])) or no_buffs_ans
        ans += f'Бафы: {buffs_str}\n' if buffs_str else ''
        buttons = [RESOURCES, MINE_BUFFS, MINE_PRICES] if 'Mine' in name \
            else [GP_BUFFS, GP_PRICES]
        # ruins have unique resource type and no buffs, so no need to change info
        if 'Ruins' not in name:
            markup = loc_info_keyboard(buttons, code)
    else:  # => instance of Alliance
        guilds = capture_info["guilds"]
        guilds_quant = len(guilds) or "неизвестно"
        ans += f'Гильдий (примерно): {guilds_quant}\n'
        guild_tags = list(map(lambda guild: guild.tag, guilds))
        guild_tags = ("<b>" + "</b> <b>".join(guild_tags) +
                      "</b>") or "неизвестно"
        ans += f'Состав (приблизительный): {guild_tags}\n'
        ans += f'Набрано очков за сезон: {capture_info["points"]}\n'
    ans += f'Последние битвы: /hist_{code}'

    await message.answer(ans, reply_markup=markup)
