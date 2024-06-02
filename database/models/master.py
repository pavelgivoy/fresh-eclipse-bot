from sqlalchemy import Column, String, ForeignKey, Integer, Text

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict

from .db_conn import Base


class Master(Base):
    """Table for masters"""

    __tablename__ = 'masters'

    link = Column('link', Text, primary_key=True)
    guild = Column('guild', String(3), ForeignKey(
        'guilds.tag', ondelete='SET NULL'))
    castle = Column('castle', Text)
    username = Column('username', String, unique=True)
    bs_guru = Column('bs_guru', Text)
    bs_level = Column('bs_level', Integer)
    alch_guru = Column('alch_guru', Text)
    alch_level = Column('alch_level', Text)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
