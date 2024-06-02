from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

from database.methods.captures import get_alliance_by_owner
from database.methods import guild
from filters.chat_filter import ChatFilter
from filters.forward_filter import ForwardFilter
from parsers.guilds import parse_guild_info, parse_guilds_list
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.alliance_guilds_list_text import ALLIANCE_GUILDS_LIST_TEXT
from utils.game_staff.answers import GUILD_INFO_UPDATE_DONE, GUILD_INFO_UPDATE_ERROR_DEV, GUILD_INFO_UPDATE_ERROR_USER, GUILD_UNKNOWN, GUILDS_ALLIANCE_NOT_FOUND, GUILDS_ALLIANCE_UPDATE_INFO_DONE, GUILDS_ALLIANCE_UPDATE_INFO_ERROR_DEV, GUILDS_ALLIANCE_UPDATE_INFO_ERROR_USER, PROVIDE_ACTUAL_FORWARD
from utils.game_staff.ids import CW_BOT_ID
from utils.game_staff.guild_profile_text import GUILD_PROFILE_TEXT


@dp.message_handler(ForwardFilter(from_ids=[CW_BOT_ID], interval=24*60*60),
                    Text(startswith=ALLIANCE_GUILDS_LIST_TEXT),
                    ChatFilter(chat_groups=['super', 'war', 'admin']),)
async def process_edit_guilds_list(message: types.Message):
    guilds = parse_guilds_list(message.text)
    guild_tags = list(map(lambda cur_guild: cur_guild['tag'], guilds))

    alliance = get_alliance_by_owner(guild_tags)

    if not alliance:
        await message.answer(GUILDS_ALLIANCE_NOT_FOUND)
        return

    update_res = guild.update_guilds_alliance_info(
        guilds, alliance, guild_tags)

    if update_res == 'error':
        await notify_admins(GUILDS_ALLIANCE_UPDATE_INFO_ERROR_DEV.format(alliance.name))
        await message.answer(GUILDS_ALLIANCE_UPDATE_INFO_ERROR_USER.format(alliance.name))
    else:
        await message.answer(GUILDS_ALLIANCE_UPDATE_INFO_DONE.format(alliance.name))


@dp.message_handler(ForwardFilter(from_ids=[CW_BOT_ID], interval=24*60*60),
                    Text(contains=GUILD_PROFILE_TEXT),
                    ChatFilter(chat_groups=['super', 'war', 'admin']),)
async def process_edit_guild_info(message: types.Message):
    parsed_guild_info = parse_guild_info(message)
    guild_tag = parsed_guild_info['tag']
    cur_guild = guild.get(guild_tag)
    if not cur_guild:
        await message.answer(GUILD_UNKNOWN.format(guild_tag))
        return

    cur_guild.name = parsed_guild_info['name']
    cur_guild.castle = parsed_guild_info['castle']
    cur_guild.emoji = parsed_guild_info['emoji']
    cur_guild.level = parsed_guild_info['level']
    cur_guild.glory = parsed_guild_info['glory']
    cur_guild.total_players = parsed_guild_info['total_players']

    update_res = guild.update([cur_guild])
    if update_res == 'error':
        await notify_admins(GUILD_INFO_UPDATE_ERROR_DEV.format(guild_tag))
        await message.answer(GUILD_INFO_UPDATE_ERROR_USER)
    else:
        await message.answer(GUILD_INFO_UPDATE_DONE)


@dp.message_handler(Text(contains=GUILD_PROFILE_TEXT) |
                    Text(startswith=ALLIANCE_GUILDS_LIST_TEXT),
                    ChatFilter(chat_groups=['super', 'war', 'admin']))
async def process_deprecated_profiles(message: types.Message):
    await message.answer(PROVIDE_ACTUAL_FORWARD.format('дня'))
