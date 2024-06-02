import re

from aiogram import types

from loader import dp
from database.methods import captures, history
from utils.game_staff.answers import UNKNOWN_CAPTURE
from utils.game_staff.date_formats import HISTORY_DATE_FORMAT
from utils.game_staff.reports_emojis import HQ_REPORTS_EMOJIS, LOC_REPORTS_EMOJIS


@dp.message_handler(regexp=r'^/hist[_ ]([a-zA-Z0-9]{6}|unknown_\d{1,4})$',
                    chat_groups=['super', 'war', 'admin'])
async def process_hist_command(message: types.Message):
    code = re.split(r'[_ ]', message.text, maxsplit=1)[-1]
    capture = captures.get_by_code(code)
    if not capture:
        await message.answer(UNKNOWN_CAPTURE.format(code))
        return

    posts = history.get_all(capture_ids=[capture.id])

    is_location = 'lvl.' in capture.name

    loc_type = 'локации' if is_location else 'альянса'
    result_emojis = LOC_REPORTS_EMOJIS if is_location else HQ_REPORTS_EMOJIS
    ans = f'История {loc_type} <b>{capture.name}</b> <code>{capture.code}</code>\n'
    last_seen = 'никогда' if len(posts) == 0 \
        else posts[-1].date.strftime(HISTORY_DATE_FORMAT)
    ans += f'Последний раз в сводках: {last_seen}\n'

    if posts:
        sliced_posts = posts[:] if len(posts) < 21 else posts[-21:]
        for entry in sliced_posts:
            ans += entry.date.strftime(HISTORY_DATE_FORMAT) + \
                ' - ' + ''.join(result_emojis[entry.result])
            if 'lvl.' in capture.name:
                ans += ' - ' + entry.owner + '\n'
            else:
                ans += ' - ' + str(entry.stock) + '📦 - ' + \
                    str(entry.glory) + '🎖\n'

    await message.answer(ans)
