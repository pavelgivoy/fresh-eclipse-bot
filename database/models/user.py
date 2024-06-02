from sqlalchemy import Column, Text, BigInteger

from .db_conn import Base
from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict


class User(Base):
    """Table for users"""

    __tablename__ = 'users'

    id = Column('id', BigInteger, primary_key=True)
    username = Column('username', Text, unique=True)

    def __str__(self) -> str:
        return pack_obj_info_into_dict(self)
