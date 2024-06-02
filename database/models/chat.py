from sqlalchemy import Column, Integer, BigInteger, Text, String, Boolean, ForeignKey


from .db_conn import Base

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict


class Chat(Base):
    """Table for chats"""

    __tablename__ = 'chats'

    id = Column('id', BigInteger, primary_key=True)
    group = Column('group', Text, nullable=False, default='not allowed')
    guild = Column('guild', String(3), ForeignKey('guilds.tag',
                                                  ondelete='CASCADE'))
    alliance = Column('alliance', Integer, ForeignKey('alliances.id',
                                                      ondelete='CASCADE'))
    locations_review_allowed = Column('locations_review_allowed',
                                      Boolean, default=True)
    withdrawing_allowed = Column('withdrawing_allowed', Boolean, default=True)
    triggers_allowed = Column('triggers_allowed', Boolean, default=True)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
