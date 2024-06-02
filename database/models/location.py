from http import server
from sqlalchemy import Column, Integer, Text, Boolean

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict

from .db_conn import Base


class Location(Base):
    """Table for locations"""

    __tablename__ = 'locations'

    id = Column('id', Integer, primary_key=True)
    code = Column('code', Text, unique=True, nullable=False)
    name = Column('name', Text, nullable=False)
    type = Column('type', Text, nullable=False)
    seen = Column('seen', Boolean, nullable=False, default=False)
    life_time = Column('life_time', Integer, nullable=False, default=0)
    owned_time = Column('owned_time', Integer, nullable=False, default=0)
    # id 1 responds to Неизвестные силы
    owner = Column('owner', Integer, nullable=False, default=1)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
