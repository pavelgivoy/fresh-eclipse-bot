def is_user_id(number: str) -> bool:
    """Define if number is bigger than zero (which means that we can parse the string into digits directly without any changes)

    :param str number: the given string
    :return bool: check result
    """
    return number.isdigit()
