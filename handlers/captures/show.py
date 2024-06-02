from aiogram import types
from database.models.alliance import Alliance

from loader import dp
from database.methods.captures import get_all_active_alliances, get_all_owned_locations, get_all_locations, get_owner
from utils.funcs.capture_template import capture_template, capture_types


@dp.message_handler(commands=['list'], chat_groups=['super', 'war', 'admin'])
async def process_list_locations(message: types.Message, basic_alliance: Alliance):
    ans = 'Актуальная информация по доступным локациям:'

    alliances = get_all_active_alliances()

    for alliance in alliances:
        emoji = capture_types['alliance']
        command = '/ga_def' if basic_alliance and alliance.name == basic_alliance.name else '/ga_atk'
        locations = get_all_owned_locations(alliance.id)
        # if forbidden and unknown forces don't have owned locations, skip them in review
        if alliance.id in (1, 2) and not locations:
            continue
        ans += '\n\n' + capture_template(emoji, command,
                                         alliance.code, alliance.name)
        for location in locations:
            emoji = capture_types[location.type]
            ans += '\n    ' + capture_template(emoji, command, location.code, location.name,
                                               location.seen, location.life_time, location.owned_time)

    await message.answer(ans)


@dp.message_handler(commands=['map'], chat_groups=['super', 'war', 'admin'])
async def process_list_alliances(message: types.Message,
                                 basic_alliance: Alliance):
    ans = 'Актуальная информация по доступным локациям:\n'

    locations = get_all_locations()
    for location in locations:
        emoji = capture_types[location.type]
        command = '/ga_def' if location.owner == basic_alliance.id else '/ga_atk'
        ans += '\n' + capture_template(emoji, command, location.code, location.name,
                                       location.seen, location.life_time, location.owned_time)
        alliance = get_owner(location.owner)
        emoji = capture_types['alliance']
        ans += '\n    ' + capture_template(emoji, command,
                                           alliance.code, alliance.name)

    await message.answer(ans)
