from sqlalchemy import Column, Integer, Text, Boolean, Float
from sqlalchemy.orm import relationship

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict

from .db_conn import Base


class Alliance(Base):
    """Table for alliances"""

    __tablename__ = 'alliances'

    id = Column('id', Integer, primary_key=True)
    code = Column('code', Text, nullable=False, unique=True)
    name = Column('name', Text, nullable=False, unique=True)
    # None means that we don't know the owner. It essentially can't be None
    owner = Column('owner', Text, default=None)
    pouches = Column('pouches', Integer, nullable=False, default=0)
    points = Column('points', Float, nullable=False, default=0)
    active = Column('active', Boolean, nullable=False, default=True)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
