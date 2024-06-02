from aiogram import types
from database.models.master import Master

from loader import dp
from utils.game_staff.basic_hq import BASIC_HQ_ID
from utils.game_staff.castles import CASTLES_REVERSED
from utils.game_staff.guru_specs import GURU_SPECS

from database.methods import master
from utils.game_staff.levels import LEVELS_REVERSED
from utils.game_staff.links import LONG_LINK, SHORT_LINK


def guru_info(spec: str, shops: list[Master]) -> str:
    """Установить выводной текст для информации о гуру альянса.

    :param str spec: специализация мастера
    :param list[Master] shops: список лавок
    :return str: стилизованный список лавок
    """
    spec_shops = sorted(filter(lambda shop: shop.bs_guru ==
                               spec or shop.alch_guru == spec, shops),
                        reverse=True)
    if not spec_shops:
        return ''
    ans = f"\n\n<b>{spec} Guru</b>"
    for guru in spec_shops:
        # a master can have multiple (one alch and one bs) gurus
        level = guru.alch_level if guru.alch_guru == spec else guru.bs_level
        level = LEVELS_REVERSED[level]
        link = guru.link
        castle = CASTLES_REVERSED[guru.castle]
        guild = guru.guild
        username = guru.username
        ans += (
            f'\n{level}'
            f' <a href="{LONG_LINK}{link}">{link}</a>'
            f' {castle} {guild} <a href="{SHORT_LINK}/{username}">@{username}</a>'
        )

    return ans


@dp.message_handler(commands=['our_guru'], chat_groups=['super', 'war', 'admin', 'allowed'], chat_alliances=[BASIC_HQ_ID])
async def show_guru(message: types.Message):
    ans = (
        'Лавки кузнецов и алхимиков нашего альянса.\n'
        'Уровень показан без учёта бафа на крафт'
    )

    for spec in GURU_SPECS:
        ans += guru_info(spec, master.get_all())

    await message.answer(ans)
