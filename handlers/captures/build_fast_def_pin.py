from aiogram import types

from loader import dp
from filters.chat_filter import ChatFilter
from database.methods.captures import get_all_owned_locations, get_basic_alliance_info
from utils.funcs.capture_template import capture_command_template
from utils.funcs.get_battle_time import get_next_battle_time
from utils.funcs.repr_level import repr_level
from utils.game_staff.answers import GO_DEF_CAPTURE
from utils.game_staff.date_formats import PIN_DATE_FORMAT


@dp.message_handler(commands=['def', 'attack'],
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=True,
                    chat_single_alliance=True)
@dp.message_handler(regexp=r"(?i)^(?:хочу (?:в )?)(?:атак|деф)(?:ы|и|у|а|(?:ов)?ать)?[.!]?$",
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=True,
                    chat_single_alliance=True)
async def build_fast_def_pin(message: types.Message, basic_alliance):
    ans = GO_DEF_CAPTURE if 'атак' in message.text or 'attack' in message.text else ''

    ans += get_next_battle_time(message.date).strftime(PIN_DATE_FORMAT)
    ans += '\n\n🛡' + capture_command_template('/ga_def',
                                              basic_alliance.code,
                                              basic_alliance.name)

    our_locations = get_all_owned_locations(basic_alliance.id)
    # sort locations by their level (names end with 'lvl.{number}')
    our_locations.sort(key=lambda x: int(x.name[-2:]), reverse=True)

    for location in our_locations:
        ans += f'\n\n{repr_level(int(location.name[-2:]))} 🛡' + \
            capture_command_template('/ga_def', location.code, location.name)

    await message.answer(ans)
