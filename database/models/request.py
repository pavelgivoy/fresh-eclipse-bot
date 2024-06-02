from sqlalchemy import Column, Integer, Text

from .db_conn import Base
from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict


class Request(Base):
    """Table for requests"""

    __tablename__ = 'requests'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', Text, nullable=False)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
