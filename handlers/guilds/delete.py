from aiogram import types

from loader import dp

from database.methods.guild import get
from database.methods.captures import get_by_code
from database.methods.guild import update_single_guild_alliance_info
from parsers.guilds import parse_delete_guild_command
from utils.game_staff.answers import GUILD_DELETE_MANUALLY_ERROR, GUILD_DELETE_MANUALLY_NO_ARGS, GUILD_IN_BASIC_ALLIANCE, GUILD_UNKNOWN
from utils.game_staff.basic_hq import BASIC_HQ_CODE, BASIC_HQ_NAME


@dp.message_handler(commands=['delete_guild'], chat_groups=['super'])
async def process_manual_delete_guild(message: types.Message):
    """Set alliance of guild and guild related info as None. Works only for Fresh Eclipse alliance

    :param types.Message message: message with the command
    """
    tag = parse_delete_guild_command(message.get_args().upper())
    if not tag:
        await message.answer(GUILD_DELETE_MANUALLY_NO_ARGS)
        return

    guild = get(tag)
    if not guild:
        await message.answer(GUILD_UNKNOWN.format(tag))
        return

    basic_alliance = get_by_code(BASIC_HQ_CODE)
    if guild.alliance != basic_alliance.id:
        await message.answer(GUILD_IN_BASIC_ALLIANCE.format(tag, 'не', BASIC_HQ_NAME))
        return

    update_res = update_single_guild_alliance_info(guild, None)
    if update_res == 'error':
        ans = GUILD_DELETE_MANUALLY_ERROR
    else:
        ans = (
            f"[{tag}], спасибо вам за верную службу, но, к сожалению, наши пути расходятся. "
            "Удачи, и до встречи на полях сражений!"
        )
    await message.answer(ans)
