import re

from aiogram import types

from utils.funcs.is_chat_id import is_chat_id
from utils.game_staff.regexps import GUILD_TAG


def parse_add_chat_command(message: types.Message) -> tuple[int | None,
                                                            str | None,
                                                            str | None,
                                                            str | None]:
    """parse arguments for /add_chat command

    :param types.Message message: message with command
    :return tuple[int | None, str | None, str | None, str | None]: parsed command arguments which represent chat id (required), chat group (optional), guild tag (optional) and alliance code (optional)
    """
    # structure of command arguments
    # {chat id} {group} {guild} {alliance code}
    chat_id = group = guild_tag = alliance_code = None
    args = message.get_args()
    if not args:
        return chat_id, group, guild_tag, alliance_code
    args = args.split(' ')
    if len(args) not in range(1, 4):
        return chat_id, group, guild_tag, alliance_code

    if is_chat_id(args[0]):
        chat_id = int(args[0])
    if len(args) >= 2:
        group = args[1]
    if len(args) == 3:
        alliance_code = args[2]
    if len(args) >= 4 and re.match(GUILD_TAG, args[3]):
        guild_tag = args[3]

    return chat_id, group, guild_tag, alliance_code


def parse_chat_id_info(message: types.Message) -> int | None:
    args = message.get_args()
    chat_id = None if not args or not is_chat_id(args) else int(args)
    return chat_id
