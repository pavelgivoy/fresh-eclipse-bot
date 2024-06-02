from aiogram import types

from database.models.chat import Chat
from database.methods import guild, user
from database.models.user_and_guild import UserAndGuild
from filters.chat_filter import ChatFilter
from keyboards.captures.build_pin_notify_keyboard import build_pin_notify_keyboard
from loader import dp
from utils.game_staff.answers import ALL_GUILDS_MARKED, GUILD_MARKED, THANKS, UNKNOWN_REPR
from utils.game_staff.basic_hq import BASIC_HQ_ID


@dp.message_handler(content_types=types.ContentTypes.PINNED_MESSAGE,
                    is_battle_order=True,
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_pinned_order_message(message: types.Message,
                                       chat: Chat):
    guilds = guild.get_all(alliances=[chat.alliance])
    guilds = map(lambda cur_guild: cur_guild.tag, guilds)
    guilds = ' '.join(guilds)

    await message.reply('Не прожались:\n' + guilds, reply_markup=build_pin_notify_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'got_pin',
                           chat_groups=['super', 'war', 'admin'],
                           chat_alliances=[BASIC_HQ_ID])
async def process_got_pin_callback(callback_query: types.CallbackQuery):
    from_user = callback_query.from_user
    user_and_guilds = user.get_all(
        user_id=from_user.id, column=UserAndGuild.guild)
    if not user_and_guilds:
        await callback_query.answer(UNKNOWN_REPR.format(from_user.username))
        return
    user_and_guilds = list(map(lambda guild: guild[0], user_and_guilds))
    text_base, msg_guilds = callback_query.message.text.split('\n')
    msg_guilds = msg_guilds.split()
    text_base += '\n'
    text = text_base + ' '.join(
        filter(lambda guild: guild not in user_and_guilds, msg_guilds))
    if text == callback_query.message.text:
        await callback_query.answer(GUILD_MARKED)
        return
    elif text == text_base:
        await callback_query.message.edit_text(ALL_GUILDS_MARKED)
    else:
        await callback_query.message.edit_text(
            text, reply_markup=build_pin_notify_keyboard())
    await callback_query.answer(THANKS)


@dp.message_handler(commands=['ping'],
                    is_reply=True,
                    chat_groups=['super', 'war', 'admin'],
                    chat_alliances=[BASIC_HQ_ID])
async def process_ping_command(message: types.Message,
                               reply: types.Message):
    left_guilds = reply.text.splitlines()[-1].split()
    for guild in left_guilds:
        guild_reprs = user.get_all(
            guild=guild, column=UserAndGuild.user_id)
        guild_reprs = user.get_all(user_ids=guild_reprs)
        ans = ' '.join(map(lambda guild_repr: '@' +
                       guild_repr.username, guild_reprs))
        await message.answer(ans)
