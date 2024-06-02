import re

from aiogram import types
from functools import reduce

from loader import dp
from database.models.guild import Guild
from database.methods.guild import get_found_and_omited_guilds
from filters.chat_filter import ChatFilter
from utils.funcs.repr_level import repr_level
from utils.game_staff.answers import OMITED_GUILDS_WARNING
from utils.game_staff.basic_hq import BASIC_HQ_ID


def stats_reduce_template(msg: str,
                          next_item: tuple[str, list[Guild]] | tuple[Guild, list[str]]) -> str:
    cur_msg = ''
    # iterate through strings (levels)
    # answer string structure: {range}\n{guild tag}: {players}
    if isinstance(next_item[0], str):
        lvl_range, guilds = next_item
        cur_msg += f'\n<code>{lvl_range}</code>\n'
        lvl_range = re.sub(r'[-+]', '', lvl_range)
        total_active_players = 0
        total_players = 0  # total players to count their activity
        for guild in guilds:
            emoji = guild.emoji or ''
            active_players = guild.__getattribute__(
                'active_players_' + lvl_range)
            cur_msg += f'{emoji}<b>{guild.tag}</b>: {active_players}\n'
            total_active_players += active_players
            total_players += guild.__getattribute__(
                'total_players_' + lvl_range)
        if total_players == 0:
            return msg
        cur_msg += f'<code>Всего</code>: {total_active_players}\n'
        cur_msg += f'<code>Активность игроков</code>: {total_active_players/total_players*100:.0f}%\n'
    # iterate through guilds
    # answer string structure: {guild tag}:\n{range}: {players}
    else:
        guild, lvl_ranges = next_item
        emoji = guild.emoji or ''
        cur_msg += f'\n{emoji}<b>{guild.tag}</b>\n'
        total_active = 0
        total = 0  # total players to count their activity
        for lvl_range in lvl_ranges:
            active_players = guild.__getattribute__(
                'active_players_' + re.sub(r'[-+]', '', lvl_range))
            total_active += active_players
            total_players = guild.__getattribute__(
                'total_players_' + re.sub(r'[-+]', '', lvl_range))
            total += total_players
            cur_msg += f'<code>{lvl_range}</code>: {active_players}\n'
        if total == 0:
            return msg
        cur_msg += f'<code>Всего</code>: {total}\n'
        cur_msg += f'<code>Активность игроков</code>: {total_active/total*100:.0f}%\n'

    return msg + cur_msg


@dp.message_handler(commands=['guild_stats'],
                    chat_groups=['super', 'war'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_show_guild_stats(message: types.Message):
    found_guilds, omited_guilds = get_found_and_omited_guilds(
        message.get_args().split())

    if omited_guilds:
        await message.answer(OMITED_GUILDS_WARNING.format('</b> <b>'.join(omited_guilds)))

    reply_msg = ''
    atk_summa = 0
    def_summa = 0
    # sort stats by guild attack
    for guild in sorted(found_guilds, lambda x: x.total_attack, reverse=True):
        emoji = guild.emoji or ''
        tag = guild.tag
        atk_stats = guild.total_attack
        def_stats = guild.total_def
        atk_summa += atk_stats
        def_summa += def_stats
        reply_msg += f"\n{emoji}{tag}: {atk_stats}⚔️ {def_stats}🛡"
    reply_msg += f"\nВсего: {atk_summa}⚔️ {def_summa}🛡"
    await message.answer(reply_msg)


@dp.message_handler(commands=['range'],
                    chat_groups=['super', 'war'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_range_command(message: types.Message):
    arg = message.get_args().upper()
    arg_list = arg.split()

    # level ranges which should be shown
    lvls = list(filter(lambda arg: arg.isdigit()
                and abs(int(arg) <= 80), arg_list))
    lvl_ranges = list(map(lambda lvl: repr_level(int(lvl)).strip(
        '</code>'), lvls)) or ['20-40', '40-60', '60+']
    lvl_ranges = sorted(list(set(lvl_ranges)),
                        key=lambda lvl_range: int(lvl_range[:2]))

    found_kws = []
    if 'GUILDS' in arg_list:
        found_kws.append('GUILDS')
        arg_list.remove('GUILDS')
    if 'LEVELS' in arg_list:
        found_kws.append('LEVELS')
        arg_list.remove('LEVELS')

    found_guilds, omited_guilds = get_found_and_omited_guilds(arg_list)
    # levels might be the guild tags, but levels-tags make users confused
    omited_guilds = list(filter(lambda guild: not (
        guild.isdigit() and abs(int(guild)) <= 80), omited_guilds))

    if omited_guilds:
        await message.answer(OMITED_GUILDS_WARNING.format('</b> <b>'.join(omited_guilds)))

    if ('LEVELS' in found_kws and 'GUILDS' in found_kws) or ('LEVELS' not in found_kws and 'GUILDS' not in found_kws):
        reply_msg = 'Ранговый состав альянса (по уровням):\n'
        # pseudo guild with accumulated stats
        pseudo_guild = Guild(tag='NULL', name='Unknown', castle='')
        for lvl_range in lvl_ranges:
            lvl_range = re.sub(r'[-+]', '', lvl_range)
            active_players = 'active_players_' + lvl_range
            pseudo_guild.__setattr__(active_players,
                                     sum(map(lambda guild: guild.__getattribute__(active_players), found_guilds)))
            total_players = 'total_players_' + lvl_range
            pseudo_guild.__setattr__(total_players,
                                     sum(map(lambda guild: guild.__getattribute__(total_players), found_guilds)))
        reduce_tuple_list = list(
            map(lambda item: (item, lvl_ranges), [pseudo_guild]))

    elif 'GUILDS' in found_kws:
        reply_msg = 'Ранговый состав альянса (по гильдиям):\n'
        reduce_tuple_list = list(
            map(lambda item: (item, lvl_ranges), found_guilds))

    elif 'LEVELS' in found_kws:
        reply_msg = 'Ранговый состав альянса (по уровням):\n'
        reduce_tuple_list = list(
            map(lambda item: (item, found_guilds), lvl_ranges))

    reply_msg = reduce(stats_reduce_template, reduce_tuple_list, reply_msg)
    if 'NULL' in reply_msg:  # clear pseudo guild name
        reply_msg = reply_msg.replace('NULL\n', '')

    await message.answer(reply_msg)
