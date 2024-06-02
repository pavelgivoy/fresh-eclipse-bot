from typing import Any, Dict

from aiogram import types
from aiogram.dispatcher.filters import Filter

from database.methods import user, user_and_chat
from database.methods.chat import get_chat_info


class UserFilter(Filter):

    def __init__(self, user_groups: list[str] | None = None,
                 user_guilds: bool | list[str] | None = None,
                 user_alliances: bool | list[str] | None = None,
                 user_is_admin: bool | None = None) -> None:
        """Initialize filter class instance

        :param list[str] user_groups: groups which user can be belonged to be able to interact with the bot, defaults to None (set default user_groups 'super', 'war' , 'admin' and 'allowed')
        :param bool | list[str] user_guilds: guilds which user can be belong to be able to interact with the bot, defautls to None (skip the filter). True means that user should be a member of any guild
        :param bool | list[str] alliances: basic alliances which user can be belong to be able to interact with the bot, defautls to None (skip the filter). True means that user should be a member of any alliance
        """
        self.user_groups = user_groups or ['super', 'war', 'admin', 'allowed']
        self.user_guilds = user_guilds
        self.user_alliances = user_alliances
        self.user_is_admin = user_is_admin

    @classmethod
    def validate(cls, full_config: Dict[str, Any]) -> Dict[str, Any]:
        config = {}
        if 'user_groups' in full_config:
            config['user_groups'] = full_config.pop('user_groups')
        if 'user_alliances' in full_config:
            config['user_alliances'] = full_config.pop('user_alliances')
        if 'user_guilds' in full_config:
            config['user_guilds'] = full_config.pop('user_guilds')
        if 'user_is_admin' in full_config:
            config['user_is_admin'] = full_config.pop('user_is_admin')
        return config

    async def check(self, update: types.Message | types.CallbackQuery) -> bool:
        """Check if user has permissible bot interaction level

        :param types.Message message: message which consists user who should be checked
        :return bool: True if check is done successfully, else False
        """
        message = update if isinstance(
            update, types.Message) else update.message
        chat = get_chat_info(update.from_user.id,
                             groups=self.user_groups,
                             guilds=self.user_guilds,
                             alliances=self.user_alliances)
        if chat == 'multiple_guilds_found':
            await message.answer('Вы состоите больше, чем в одной гильдии. Для этого действия нужны точные сведения о конкретной гильдии.')
            return False
        if chat == 'multiple_alliances_found':
            await message.answer('Вы состоите больше, чем в одном альянсе. Для этого действия нужны точные сведения о конкретном альянсе.')
            return False
        if not chat:
            return False
        cur_user = user.get(update.from_user.id)
        cur_user_and_chat = user_and_chat.get(
            update.from_user.id, message.chat.id)
        if self.user_is_admin and (not cur_user_and_chat or not cur_user_and_chat.is_admin):
            return False
        return {'user': cur_user,
                'user_and_chat': cur_user_and_chat}
