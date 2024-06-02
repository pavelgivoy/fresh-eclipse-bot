from .is_number import is_number


def is_chat_id(number: str) -> bool:
    """Define if the given string is the number less than zero (which means that the string is the number and this string contains a minus at the beginning)

    :param str number: the given string
    :return bool: check result
    """
    return is_number(number) and number.startswith('-')
