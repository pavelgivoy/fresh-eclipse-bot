from aiogram import types

from loader import dp
from database.models.guild import Guild
from database.methods.captures import get_by_code
from database.methods.guild import get, update, update_single_guild_alliance_info
from parsers.guilds import parse_add_guild_command
from utils.game_staff.answers import GUILD_ADD_MANUALLY_NO_ARGS, GUILD_IN_BASIC_ALLIANCE
from utils.game_staff.castles import CASTLES
from utils.game_staff.basic_hq import BASIC_HQ_CODE, BASIC_HQ_ID, BASIC_HQ_NAME


@dp.message_handler(commands=['add_guild'], chat_groups=['super'])
async def process_manual_add_guild(message: types.Message):
    """Add new guild manually. Works only for Fresh Eclipse alliance

    :param types.Message message: message with the command
    """
    guild_tag, name, castle = parse_add_guild_command(
        message.get_args().split())
    if not guild_tag or not name or not castle or castle not in CASTLES.keys():
        await message.answer(GUILD_ADD_MANUALLY_NO_ARGS)
        return

    guild = get(guild_tag)
    basic_alliance = get_by_code(BASIC_HQ_CODE)
    if guild and guild.alliance == basic_alliance.id:
        await message.answer(GUILD_IN_BASIC_ALLIANCE.format(guild_tag, 'уже', BASIC_HQ_NAME))
        return

    if guild:
        guild.name = name
        update_single_guild_alliance_info(guild, BASIC_HQ_ID)
    else:
        guild = Guild(tag=guild_tag,
                      name=name,
                      castle=castle,
                      alliance=basic_alliance.id)
        update([guild])

    ans = (
        f"Приветствую гильдию [{guild_tag}] в рядах нашего альянса!\n"
        "Да будут остры ваши мечи и клинки, сильны копья и щиты, и пусть теперь "
        "ваши бравые воины служат в наше (и своё) благо!\n"
        "<code>Отправьте мне форвард профиля гильдии для дополнения информации об уровне, глори и пр.</code>"
    )
    await message.answer(ans)
