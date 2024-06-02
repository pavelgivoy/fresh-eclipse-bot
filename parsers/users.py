import re

from utils.funcs.is_chat_id import is_chat_id
from utils.funcs.is_user_id import is_user_id
from utils.game_staff.regexps import GUILD_TAG


def parse_add_repr_command(args: list[str]) -> tuple[str | None]:
    guild = user_id = username = None
    if len(args) == 3 and re.match(GUILD_TAG, args[0].upper()) and is_user_id(args[1]):
        guild, user_id, username = args
    return guild.upper(), int(user_id), username


def parse_del_repr_command(args: list[str]) -> tuple[str | None]:
    guild = user_info = flag = None
    if len(args) >= 2:
        guild, user_info = args[:2]
        if is_user_id(user_info):
            user_info = int(user_info)
    if len(args) == 3 and '!' in args[2]:
        flag = args[2].strip('!')
    return guild.upper(), user_info, flag


def parse_user_and_chat(args: list[str]) -> tuple[str | None]:
    chat_id = user_id = None

    if len(args) > 2:
        return chat_id, user_id

    for arg in args:
        if is_chat_id(arg):
            chat_id = int(arg)
        elif is_user_id(arg):
            user_id = int(arg)

    return chat_id, user_id


def parse_list_users_and_guilds_command(args: list[str]) -> tuple[str | None]:
    user_id = guild_tag = None

    if len(args) > 2:
        return user_id, guild_tag

    for arg in args:
        if is_user_id(arg):
            user_id = int(arg)
        elif re.match(GUILD_TAG, arg):
            guild_tag = arg

    return user_id, guild_tag
