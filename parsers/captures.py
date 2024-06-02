import re

from utils.game_staff.regexps import CAPTURE_CODE, GUILD_TAG


def parse_cw_capture_info(text: str) -> tuple[str, str]:
    # text structure: "You found hidden location/headquarter <capture name>\nТо remember the route you associated it with simple combination: <capture code>"
    sep = 'headquarter' if 'headquarter' in text else 'location'
    # <capture code> is the required code
    code = text.split()[-1]
    # <capture name> is the required name
    name = text.split(sep=sep)[1].split('\n')[0].strip()
    return code, name


def parse_ga_add_command(input_info: list[str]) -> tuple[str | None, str | None]:
    # args structure: {code} {name}
    # length of code - 1 word (assume dividing input by whitespace)
    # length of name - 2-3 words
    # so, we expect 3-4 words in arguments
    if len(input_info) not in [3, 4]:
        return None, None

    return input_info[0], ' '.join(input_info[1:])


def parse_force_update_location_owner_command(args: list[str]) -> tuple[str, str]:
    code, new_owner = None, None

    if len(args) < 3 or not re.match(CAPTURE_CODE, args[0]):
        return code, new_owner

    return args[0], ' '.join(args[1:])


def parse_set_alliance_owner_command(args: list[str]) -> tuple[str, str]:
    code, new_owner = None, None

    if len(args) != 2 \
            or not re.match(CAPTURE_CODE, args[0]) \
            or not re.match(GUILD_TAG, args[1].upper()):
        return code, new_owner

    return args[0], ' '.join(args[1:])
