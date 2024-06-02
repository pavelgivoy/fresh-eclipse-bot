import re


def remove_markdowns(string: str) -> str:
    return re.sub(r"\<(/?)(code|b|i|u)\>", '', string)
