from ..game_staff.links import LONG_LINK


capture_types = {
    'mine': '⛏',
    'ruins': '🔮',
    'glory_point': '🎖',
    'alliance': '🏛',
    'forbidden': '👹',
    'undefined': '🪲',
}


def capture_history_template(emoji: str, code: str) -> str:
    return f'<a href="{LONG_LINK}/hist_{code}">{emoji}</a>'


def capture_command_template(command: str, code: str, name: str) -> str:
    if code.startswith('unknown_'):
        return name
    return f'<a href="{LONG_LINK}{command}_{code}">{name}</a>'


def capture_info_template(code: str) -> str:
    return f'<a href="{LONG_LINK}/i_{code}">ℹ️</a>'


def capture_deprecated_template(code: str) -> str:
    return f'<a href="{LONG_LINK}/ga_delete_{code}">👾</a>'


def capture_template(emoji: str,
                     command: str,
                     code: str,
                     name: str,
                     seen: bool | None = None,
                     lived: int | None = None,
                     captured: int | None = None) -> str:
    if name == 'Запретные силы':
        return capture_types['forbidden'] + name + capture_types['forbidden']
    if name == 'Неизвестные силы':
        return capture_types['undefined'] + name + capture_types['undefined']

    # seen is None means that it's alliance instance
    # seen is bool means that it's location instance
    # it's pleasant to aviod frequent own check marks in the message
    own_check = '✔️' if command == '/ga_def' and seen is None else ''
    history_info = capture_history_template(emoji, code)
    command_info = capture_command_template(command, code, name)
    extra_info = f'{lived}|{captured}' if seen is not None else ''
    cdt_info = capture_deprecated_template(code) if seen == False else ''
    return own_check + history_info + \
        command_info + \
        cdt_info + ' ' + \
        extra_info + \
        capture_info_template(code)
