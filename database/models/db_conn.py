from psycopg2.extensions import register_adapter, AsIs
from sqlalchemy import create_engine, Row
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Any

from utils.configs.db_conn_string import CONN_STRING


Base = declarative_base()


class DatabaseConnection:
    """SQLAlchemy database connection"""

    def __init__(self) -> None:
        # adapter which transfrom returning SQL query result instance
        # from (obj,) to obj
        register_adapter(Row, self.adapt_returned_tuples)
        self.engine = create_engine(CONN_STRING)
        temp_session = sessionmaker()
        self.session = temp_session(bind=self.engine)

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()

    def adapt_returned_tuples(self, sequence: tuple[Any]) -> Any:
        """Adapt returned tuples after SQL statement executing from tuples (obj,) to obj instance

        :param tuple[Any] sequence: any one member tuple
        :return Any: parsed object from tuple
        """
        ans_seq = sequence[0] if len(sequence) == 1 else sequence
        return AsIs(ans_seq)
