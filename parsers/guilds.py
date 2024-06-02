import re

from utils.game_staff.castles import CASTLES
from utils.game_staff.regexps import GUILD_TAG


def parse_add_guild_command(args: list[str]) -> tuple[str | None, str | None, str | None]:
    guild_tag = name = castle = None
    if len(args) < 3:
        return guild_tag, name, castle

    if re.match(GUILD_TAG, args[0]):
        guild_tag = args[0]
    name = ' '.join(args[2:])
    castle = args[1]

    return guild_tag, name, castle


def parse_delete_guild_command(args: str | None) -> str | None:
    tag = None
    if not args:
        return tag

    if re.match(GUILD_TAG, args):
        tag = args

    return tag


def parse_guild_info(text: str) -> dict[str, int | str | None]:
    guild: dict[str, int | str | None] = {
        'tag': None,
        'name': None,
        'emoji': None,
        'level': None,
        'glory': None,
        'castle': None,
    }
    lines = text.splitlines()
    initial_info = lines[0]
    guild['tag'], guild['name'] = initial_info.split('[')[-1].split(']')
    # it's impossible to set initial_info[0] or initial_info[1] to castle emoji, because emoji length might be 1 or 2 chars
    # so available solution is iterating through existing castle emojis to find that one which line contains
    for castle in CASTLES.keys():
        if castle in initial_info:
            guild['castle'] = castle
    # undefined emoji length problem is actual here too
    # remove castle emoji from line and search for guild emoji
    # it should be placed between castle emoji and begin of guild tag
    guild['emoji'] = initial_info.split('[')[0].lstrip(guild['castle'])

    glory_and_level = lines[2]
    level, glory = glory_and_level.split('🎖')
    guild['level'] = int(level.split('Level: ')[-1].strip())
    guild['glory'] = int(glory.split('Glory: ')[-1].split('/')[-1])
    guild['total_players'] = int(lines[-1].split('/')[0].lstrip('👥 '))

    return guild


def parse_guilds_list(text: str) -> list[dict[str, str | None]]:
    guilds = []
    lines = text.splitlines()
    for line in lines[1:]:
        guild = {}
        guild['tag'], guild['name'] = line.split('[')[-1].split(']')
        # it's impossible to set line[0] or line[1] to castle emoji, because emoji length might be 1 or 2 chars
        # so available solution is iterating through existing castle emojis to find that one which line contains
        for castle in CASTLES.keys():
            if castle in line:
                guild['castle'] = castle
        # undefined emoji length problem is actual here too
        # remove castle emoji from line and search for guild emoji
        # it should be placed between castle emoji and begin of guild tag
        guild['emoji'] = line.split('[')[0].lstrip(guild['castle'])
        guilds.append(guild)

    return guilds


def parse_guild_roster(text: str):
    lines = text.splitlines(keepends=True)
    guild_and_castle, roster_text = lines[0], ''.join(lines[1:])

    guild_name = roster = None

    guild_and_castle_regexp = re.compile(
        r'^([🖤🍆🐢🌹🦇☘️🍁])(.{4,16})$', flags=re.UNICODE | re.MULTILINE)
    guild_name = guild_and_castle_regexp.search(guild_and_castle)
    if guild_name:
        guild_name = guild_name.group(2)

    roster_regexp = re.compile(
        r"^#\d{1,2}\s[📦⚔️️⚗️🛠🛡🏹🎩🩸]{1,4}(\d{2})\s\[([🛌🌲🍄⛰⚒🏹🛡⚔️⚗️📦🗡💤]{1,2})\]\s.{4,16}$", flags=re.UNICODE | re.MULTILINE)
    roster = roster_regexp.findall(roster_text)

    return guild_name, roster
