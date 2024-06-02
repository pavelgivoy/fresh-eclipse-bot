from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from database.methods.user_and_chat import get
from parsers.chats import parse_chat_id_info
from utils.funcs.remove_markdowns import remove_markdowns
from utils.game_staff.answers import CHAT_SETTING_CHANGING_NOT_ALLOWED


class UserIsAdminOfInputChat(BoundFilter):
    key = 'user_is_admin_of_input_chat'
    required = False
    default = False

    def __init__(self, user_is_admin_of_input_chat: bool = False) -> None:
        self.user_is_admin_of_input_chat = user_is_admin_of_input_chat

    async def check(self, update: types.Message | types.CallbackQuery) -> bool:
        """Check if user is admin of input chat

        :param types.Message | types.CallbackQuery update: incoming instance (message or callback query)
        :return bool: True if check is done successfully, else False
        """
        if not self.user_is_admin_of_input_chat:
            return False
        # user instance and answer method are referenced to update type directly
        # chat instance is referenced to message type only
        is_message = isinstance(update, types.Message)
        message = update if is_message else update.message
        chat_id = parse_chat_id_info(
            message) if message.chat.type == types.ChatType.PRIVATE else message.chat.id
        user_and_chat = get(update.from_user.id,
                            chat_id)
        if not user_and_chat or not user_and_chat.is_admin:
            ans = CHAT_SETTING_CHANGING_NOT_ALLOWED.format(chat_id)
            if not is_message:
                ans = remove_markdowns(ans)

            if is_message:
                await update.answer(ans)
            else:
                await update.answer(ans, show_alert=True)
            return False
        return True
