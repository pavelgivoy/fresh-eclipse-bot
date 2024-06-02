def repr_level(level: int | str) -> str:
    level = int(level)
    low = level - (level % 20)
    high = low + 20
    return '<code>' + str(low) + '-' + str(high) + '</code>' if high != 80 else '<code>60+</code>'
