from sqlalchemy import Column, BigInteger, String, ForeignKey

from .db_conn import Base
from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict


class UserAndGuild(Base):
    """Table for users and guilds matches"""

    __tablename__ = 'users_and_guilds'

    user_id = Column('user_id', BigInteger, ForeignKey('users.id',
                                                       ondelete='CASCADE'), primary_key=True)
    guild = Column('guild', String(3), ForeignKey('guilds.tag',
                                                  ondelete='CASCADE'), primary_key=True)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
