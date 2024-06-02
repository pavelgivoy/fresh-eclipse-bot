from .states import dp
from .gurus import dp
from .battle_reports import dp
from .captures import dp
from .chats import dp
from .guilds import dp
from .requests import dp
from .users import dp
# MUST be the last import!!! Otherwise, further imports might be ignored
from .triggers import dp

__all__ = ['dp']
