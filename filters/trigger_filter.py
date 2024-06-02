from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from database.methods import trigger


class TriggerFilter(BoundFilter):
    """This class checks that message contains a trigger"""

    async def check(self, message: types.Message) -> bool:
        """Check that trigger in the database and in the message text

        :param types.Message message: message with the potential trigger
        :return bool: True if trigger is found in the database and message contains (or fully equals to) the one, else False
        """
        text = message.text

        global_chat_id = None
        local_chat_id = message.chat.id
        chat_ids = [global_chat_id, local_chat_id]
        triggers = trigger.get_all(chat_ids=chat_ids)

        for tr in triggers:
            if (tr.strict and text == tr.name) or (not tr.strict and tr.name in text):
                res = {}
                value = tr.text_value if tr.type == 'text' else tr.file_id
                res[tr.type] = value
                if tr.type != 'text' and tr.text_value is not None:
                    res['text'] = tr.text_value
                return res
