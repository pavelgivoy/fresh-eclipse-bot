import re
from aiogram import types

from loader import dp
from database.models.alliance import Alliance
from database.models.location import Location
from database.methods.captures import get_by_code
from utils.funcs.capture_template import capture_command_template
from utils.game_staff.answers import NOT_OWN_CAPTURE_WARNING, OWN_CAPTURE_WARNING, UNKNOWN_CAPTURE


@dp.message_handler(regexp=r'^/ga_(atk|def)_([a-zA-Z0-9]{6})?$', chat_groups=['super', 'war', 'admin'], chat_alliances=True, chat_single_alliance=True)
async def process_ga_atk_or_def_command(message: types.Message,
                                        basic_alliance: Alliance,
                                        regexp: re.Match):
    command = regexp.group(1)
    code = regexp.group(2)
    if not code:
        code = basic_alliance.code
    capture = get_by_code(code)
    if not capture:
        await message.answer(UNKNOWN_CAPTURE.format(code))
        return

    own_capture = basic_alliance and ((isinstance(capture, Alliance) and capture.id == basic_alliance.id)
                                      or (isinstance(capture, Location) and capture.owner == basic_alliance.id))

    if command == 'atk' and own_capture:
        await message.answer(OWN_CAPTURE_WARNING)
    elif command == 'def' and not own_capture:
        await message.answer(NOT_OWN_CAPTURE_WARNING)
    emoji = "⚔️" if 'atk' in message.text else "🛡"
    ans = emoji + capture_command_template(command, capture.code, capture.name)
    await message.answer(ans)
