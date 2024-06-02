from sqlalchemy import Column, BigInteger, Text, String, Boolean, ForeignKey

from utils.funcs.pack_obj_info_into_dict import pack_obj_info_into_dict

from .db_conn import Base


class Trigger(Base):
    """Table for triggers

    :param BigInteger id: trigger id
    :param BigInteger chat_id: replied message chat id
    :param BigInteger message_id: replied message id
    :param Text name: trigger name
    :param Text text_value: trigger text catched from message text or message caption (if exists)
    :param Text file_id: trigger file id for media (if exists)
    :param Boolean strict: if True, trigger will be caused when the message text is fully equal to trigger name. Otherwise, trigger will be caused when the message text contains the one.
    """

    __tablename__ = 'triggers'

    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    type = Column('type', Text, nullable=False)
    # NULL means that the trigger is global
    chat_id = Column('chat_id', BigInteger, ForeignKey('chats.id',
                                                       ondelete='CASCADE'), nullable=True)
    message_id = Column('message_id', BigInteger, nullable=False)
    name = Column('name', Text, nullable=False)
    text_value = Column('text_value', Text, nullable=True)
    file_id = Column('file_id', Text, nullable=True)
    strict = Column('strict', Boolean, nullable=False, default=False)

    def __str__(self) -> str:
        return str(pack_obj_info_into_dict(self))

    def __repr__(self) -> dict:
        return pack_obj_info_into_dict(self)
