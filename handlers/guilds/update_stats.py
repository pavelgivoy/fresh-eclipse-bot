from aiogram import types

from loader import dp

from parsers.guilds import parse_guild_roster
from database.models.guild import Guild
from database.methods.guild import get_by_name, update
from filters.chat_filter import ChatFilter
from filters.forward_filter import ForwardFilter
from filters.is_guild_roster import IsGuildRoster
from filters.is_guild_stats import IsGuildStats
from utils.game_staff.answers import GUILD_INFO_UPDATE_ERROR_DEV, GUILD_INFO_UPDATE_ERROR_USER, GUILD_ROSTER_UPDATE_DONE, GUILD_STATS_UPDATE_DONE, PROVIDE_ACTUAL_FORWARD
from utils.game_staff.basic_hq import BASIC_HQ_ID
from utils.game_staff.ids import CW_BOT_ID
from utils.funcs.notify_admins import notify_admins


async def send_result(message: types.Message, update_res: str, guild: Guild, ans: str):
    if update_res == 'error':
        await notify_admins(GUILD_INFO_UPDATE_ERROR_DEV.format(guild.tag))
        await message.answer(GUILD_INFO_UPDATE_ERROR_USER.format(guild.tag))
    else:
        await message.answer(ans)


@dp.message_handler(ForwardFilter(from_ids=[CW_BOT_ID], interval=60),
                    IsGuildRoster(),
                    ChatFilter(chat_groups=['super', 'admin'],
                               chat_alliances=[BASIC_HQ_ID]))
async def process_guild_roster(message: types.Message):
    guild_name, roster = parse_guild_roster(message.text)
    guild = get_by_name(guild_name)
    guild_tag = guild.tag
    guild.active_players_2040 = 0
    guild.active_players_4060 = 0
    guild.active_players_60 = 0
    guild.total_players_2040 = 0
    guild.total_players_4060 = 0
    guild.total_players_60 = 0

    for person in roster:
        level, state = int(person[0]), person[1]
        # minimum level for attacking locations is 20
        if level in range(20, 40):
            if state != '💤':
                guild.active_players_2040 += 1
            guild.total_players_2040 += 1
        elif level in range(40, 60):
            if state != '💤':
                guild.active_players_4060 += 1
            guild.total_players_4060 += 1
        # maximum level for game person is 80
        elif level in range(60, 81):
            if state != '💤':
                guild.active_players_60 += 1
            guild.total_players_60 += 1

    update_res = update([guild])
    await send_result(message, update_res, guild, GUILD_ROSTER_UPDATE_DONE.format(guild_tag))


@dp.message_handler(ForwardFilter(from_ids=[CW_BOT_ID], interval=60),
                    IsGuildStats(),
                    ChatFilter(chat_groups=['super', 'admin'],
                               chat_alliances=[BASIC_HQ_ID]),)
async def process_guild_stats(message: types.Message):
    summa = 0
    text = message.text
    lines = text.split('#')
    guild_name = lines[0].split('Rating')[0].strip().split()[:-1]
    guild_name = ' '.join(guild_name)[1:]
    emoji = '🛡' if 'Defence' in lines[0] else '⚔'
    for line in lines[1:]:
        value = line.split(emoji)[-1].split()[0]
        summa += int(value)

    guild = get_by_name(guild_name)
    # it's gdeflist
    if 'Defence' in lines[0]:
        guild.total_def = summa
    # it's gatklist
    else:
        guild.total_attack = summa
    update_res = update([guild])
    await send_result(message, update_res, guild, GUILD_STATS_UPDATE_DONE)


@dp.message_handler(IsGuildRoster() | IsGuildStats(),
                    ChatFilter(chat_groups=['super', 'admin'],
                               chat_alliances=[BASIC_HQ_ID]),)
async def process_deprecated_profile(message: types.Message):
    await message.answer(PROVIDE_ACTUAL_FORWARD.format('60 секунд'))
