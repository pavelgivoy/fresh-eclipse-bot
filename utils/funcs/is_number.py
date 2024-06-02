def is_number(number: str) -> bool:
    """Define if the given string is the number (which means that the string contains only digits after minus shifting from the beginning)

    :param str number: the given string
    :return bool: check result
    """
    return number.lstrip('-').isdigit()
