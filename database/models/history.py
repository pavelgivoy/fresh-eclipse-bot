from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict

from .db_conn import Base


class History(Base):
    """Table for locations and alliances history"""

    __tablename__ = 'history'

    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime, nullable=False)
    alliance_id = Column('alliance_id', Integer, ForeignKey(
        'alliances.id', ondelete='CASCADE'))
    location_id = Column('location_id', Integer, ForeignKey(
        'locations.id', ondelete='CASCADE'))
    result = Column('result', Text, nullable=False)
    stock = Column('stock', Integer)
    glory = Column('glory', Integer)
    owner = Column('owner', Text)

    @hybrid_property
    def capture_id(self) -> Column[int]:
        return self.alliance_id or self.location_id

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
