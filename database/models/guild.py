from sqlalchemy import Column, Integer, Text, String, ForeignKey

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict

from .db_conn import Base


class Guild(Base):
    """Table for guilds"""

    __tablename__ = 'guilds'

    tag = Column('tag', String(3), primary_key=True)
    name = Column('name', Text, nullable=False)
    castle = Column('castle', Text)
    emoji = Column('emoji', Text)
    level = Column('level', Integer, default=0)
    glory = Column('glory', Integer, default=0)
    total_attack = Column('total_attack', Integer, default=0)
    total_def = Column('total_def', Integer, default=0)
    active_players_2040 = Column('active_players_2040', Integer, default=0)
    active_players_4060 = Column('active_players_4060', Integer, default=0)
    active_players_60 = Column('active_players_60+', Integer, default=0)
    total_players_2040 = Column('total_players_2040', Integer, default=0)
    total_players_4060 = Column('total_players_4060', Integer, default=0)
    total_players_60 = Column('total_players_60+', Integer, default=0)
    alliance = Column('alliance', Integer, ForeignKey('alliances.id',
                                                      ondelete='SET NULL'))

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
