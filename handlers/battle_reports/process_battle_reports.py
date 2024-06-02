import datetime
import time

from aiogram import types
from aiogram.dispatcher.filters import Text
from sqlalchemy.orm.session import Session
from database.models.history import History

from loader import dp, bot
from database.methods import battle_reports
from database.methods.chat import get_all
from database.methods.common import session_handler
from filters.chat_filter import ChatFilter
from filters.forward_filter import ForwardFilter
from parsers.battle_reports import parse_hq_report, parse_map_report
from utils.game_staff.battle_reports import battle_report
from utils.funcs.get_battle_time import get_previous_battle_time
from utils.game_staff.answers import BATTLE_FOUND, BATTLE_REPORT_ERROR
from utils.game_staff.ids import CW_DIGEST_ID
from utils.game_staff.reports_emojis import HQ_REPORTS_EMOJIS, LOC_REPORTS_EMOJIS
from utils.game_staff.date_formats import BATTLE_DATE_FORMAT


def create_report_link(link_title: str, message: types.Message):
    return (
        f'\n<a href="http://t.me/{message.forward_from_chat.username}/{message.forward_from_message_id}">'
        f'{link_title}</a>\n\n'
    )


def create_text_hq_report(message: types.Message):
    text = create_report_link('🤝Headquarters news',
                              message)

    for report in battle_report.parsed_hq_report:
        prefix = ''
        for key, values in HQ_REPORTS_EMOJIS.items():
            if key == report['result']:
                prefix = ''.join(values)
        text += prefix + report['name'] + ' ' + \
            (str(report['stock']) + '📦 ' if report['stock'] else '') + \
            (str(report['glory']) + '🎖' if report['glory'] else '') + '\n'

    return text


def create_text_map_report(message: types.Message):
    text = create_report_link('🗺State of Map',
                              message)

    for report in battle_report.parsed_map_report:
        prefix = ''
        for key, values in LOC_REPORTS_EMOJIS.items():
            if key == report['result']:
                prefix = ''.join(values)
        text += prefix + report['name']
        if report['new_owner'] and report['new_owner'] != 'Запретные силы':
            text += ':\n' + '    ➡️ ' + report['new_owner']
        text += '\n'

    return text


def create_report_text(message: types.Message,
                       date: datetime.datetime):
    return f'{datetime.datetime.strftime(date, BATTLE_DATE_FORMAT)}\n\n' + \
        create_text_hq_report(message) + '\n\n' + \
        create_text_map_report(message)


async def send_report(texts: dict[int, str]):
    chats = get_all()
    msg_sent = 0
    for chat in chats:
        alliance_id = chat.alliance or 1
        text = texts[alliance_id]
        await bot.send_message(chat.id, text, disable_web_page_preview=True, disable_notification=True)
        msg_sent += 1
        # avoid Telegram API limit of 30 messages per second
        if msg_sent == 29:
            time.sleep(1)
            msg_sent = 0


@session_handler
def get_battle_reports_texts(message: types.Message, session: Session | None = None):
    date = get_previous_battle_time(message.forward_date)
    battles = session.query(History).filter_by(date=date).first()
    if battles:
        return 'found'
    battle_reports.write(date,
                         battle_report.parsed_hq_report,
                         battle_report.parsed_map_report)
    report_text = create_report_text(message, date)
    generated_texts = battle_reports.include_owners(
        report_text, session=session)
    # id = 1 is for chats without defined alliance (e.g. superchats)
    generated_texts[1] = report_text
    return generated_texts


@dp.message_handler(Text(contains=['State of map']) |
                    Text(contains=['Headquarters news:']),
                    ForwardFilter(from_ids=[CW_DIGEST_ID]),
                    ChatFilter(chat_groups=['super']))
async def process_map_report(message: types.Message):
    text = message.text
    if 'Headquarters news:' in text:
        battle_report.parsed_hq_report = parse_hq_report(text)
    else:
        battle_report.parsed_map_report = parse_map_report(text)

    # battle report must be created when both report parts received
    if battle_report.parsed_hq_report and battle_report.parsed_map_report:
        generated_texts = get_battle_reports_texts(message)
        if not generated_texts or generated_texts == 'error':
            await message.answer(BATTLE_REPORT_ERROR)
        elif generated_texts == 'found':
            await message.answer(BATTLE_FOUND)
        else:
            await send_report(generated_texts)

        battle_report.parsed_hq_report = []
        battle_report.parsed_map_report = []
