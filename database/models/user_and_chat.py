from sqlalchemy import Boolean, Column, BigInteger, ForeignKey

from .db_conn import Base
from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict


class UserAndChat(Base):
    """Table for users and chats"""

    __tablename__ = 'users_and_chats'

    user_id = Column('user_id', BigInteger, ForeignKey('users.id',
                                                       ondelete='CASCADE'),
                     primary_key=True)
    chat_id = Column('chat_id', BigInteger, ForeignKey('chats.id',
                                                       ondelete='CASCADE'),
                     primary_key=True)
    is_admin = Column('is_admin', Boolean, default=False)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
