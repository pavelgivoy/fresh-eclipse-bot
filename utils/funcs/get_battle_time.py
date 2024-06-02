import datetime


def get_previous_battle_time(time: datetime.datetime) -> datetime.datetime:
    return time - datetime.timedelta(hours=(time.hour-1) % 8,
                                     minutes=time.minute,
                                     seconds=time.second,
                                     microseconds=time.microsecond)


def get_next_battle_time(time: datetime.datetime) -> datetime.datetime:
    return get_previous_battle_time(time) + datetime.timedelta(hours=8)
