import logging
import traceback

from functools import wraps
from sqlalchemy import Row, Column
from sqlalchemy.orm import Query
from typing import Any

from ..models.db_conn import DatabaseConnection


def get_empty_id(objs: list[Row[tuple[int]]]) -> int:
    obj_ids = list(map(lambda obj: obj.id, objs))
    if not obj_ids:
        return 1

    for i in range(1, max(obj_ids) + 1):
        if i not in obj_ids:
            return i

    return max(obj_ids) + 1


def get_query_from_intervals(query: Query, column_name: Column[Any], interval: int | list[int]):
    # [a, b] -> between a and b
    if interval is list and len(interval) == 2 and interval[0] and interval[1]:
        query = query \
            .filter(column_name.between(interval[0], interval[1]))
    # [_, b] -> <= b
    elif interval is list and len(interval) == 2 and not interval[0] and interval[1]:
        query = query \
            .filter(column_name <= interval[1])
    # [a, _] (or [a], or a) -> >= a
    elif (interval is list and (len(interval) == 2 and interval[0] and not interval[1])
            or (len(interval) == 1 and interval[0])) or (interval):
        min_value = interval[0] if interval is list else interval
        query = query \
            .filter(column_name >= min_value)
    # [_, _] (or [_], or _) -> skip
    return query


def session_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        close_session = False
        # session was not received from outer scope, create db connection
        # mark that session should be closed when function is completed
        if not kwargs or 'session' not in kwargs.keys():
            session = DatabaseConnection().session
            kwargs['session'] = session
            close_session = True
        # session was received from outer scope, use it
        else:
            session = kwargs['session']

        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.error(traceback.format_exc())
            if str(func.__name__).startswith('get'):
                res = None
            else:
                session.rollback()
                res = 'error'
        else:
            # if session should be closed and method updates database, commit transactions
            # get methods don't update the database
            if close_session and not str(func.__name__).startswith('get'):
                session.commit()

        # if session was opened in the wrapper, close it
        if close_session:
            session.close()

        return res
    return wrapper
