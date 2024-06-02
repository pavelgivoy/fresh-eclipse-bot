from sqlalchemy import Column, Integer, Text, ForeignKey

from .db_conn import Base
from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict


class Resource(Base):
    """Table for location resources info"""

    __tablename__ = 'resources'

    id = Column('id', Integer, primary_key=True)
    location_id = Column('location_id', Integer,
                         ForeignKey('locations.id',
                                    ondelete='CASCADE'),
                         nullable=False)
    type = Column('type', Text, nullable=False)  # mine, glory, ruins, buffs
    # magic stone, ruby, glory/forge buff name etc.
    name = Column('name', Text, nullable=False)
    price = Column('price', Integer, default=None)  # buff price

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
