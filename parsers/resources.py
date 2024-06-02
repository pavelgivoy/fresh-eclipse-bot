from aiogram import types

from utils.game_staff.resources import GP_BUFFS, MINE_BUFFS, RESOURCES


def parse_new_resource_info(keyboard: list[list[types.InlineKeyboardButton]]):
    price = None
    buff = None
    resources = []
    for i in range(len(keyboard)):
        for j in range(len(keyboard[i])):
            btn_text = keyboard[i][j].text
            if '✅' in btn_text:
                btn_text = btn_text.replace('✅', '')
                if btn_text.isdigit():
                    price = int(btn_text)
                if btn_text in GP_BUFFS or btn_text in MINE_BUFFS:
                    buff = btn_text
                if btn_text in RESOURCES:
                    resources.append(btn_text)
    return resources, buff, price
