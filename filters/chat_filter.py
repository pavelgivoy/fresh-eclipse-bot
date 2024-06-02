from typing import Any, Dict

from aiogram import types
from aiogram.dispatcher.filters import Filter

from database.methods import captures, guild
from database.methods.chat import get_chat_info


class ChatFilter(Filter):
    """This class filters that message was received in a chat which responds to given groups, guilds and basic alliances
    """

    def __init__(self, chat_groups: list[str] | None = None,
                 chat_guilds: list[str] | None = None,
                 chat_alliances: bool | list[str] | None = None,
                 chat_single_alliance: bool = False,
                 chat_single_guild: bool = False,
                 triggers_allowed: bool | None = None) -> None:
        """Initialize filter class instance

        :param list[str] chat_groups: groups which user can be belonged to be able to interact with the bot, defaults to None (set default chat_groups 'super', 'admin' and 'allowed')
        :param list[str] chat_guilds: guilds which user can be belong to be able to interact with the bot, defautls to None (skip the filter)
        :param bool | list[str] chat_alliances: basic alliances which user can be belong to be able to interact with the bot, defautls to None (skip the filter)
        """
        self.chat_groups = chat_groups
        self.chat_alliances = chat_alliances
        self.chat_guilds = chat_guilds
        self.chat_single_alliance = chat_single_alliance
        self.chat_single_guild = chat_single_guild
        self.triggers_allowed = triggers_allowed

    @classmethod
    def validate(cls, full_config: Dict[str, Any]) -> Dict[str, Any]:
        config = {}
        if 'chat_groups' in full_config:
            config['chat_groups'] = full_config.pop('chat_groups')
        if 'chat_alliances' in full_config:
            config['chat_alliances'] = full_config.pop('chat_alliances')
        if 'chat_guilds' in full_config:
            config['chat_guilds'] = full_config.pop('chat_guilds')
        if 'chat_single_alliance' in full_config:
            config['chat_single_alliance'] = full_config.pop(
                'chat_single_alliance')
        if 'chat_single_guild' in full_config:
            config['chat_single_guild'] = full_config.pop('chat_single_guild')
        if 'triggers_allowed' in full_config:
            config['triggers_allowed'] = full_config.pop('triggers_allowed')
        return config

    async def check(self, update: types.Message | types.CallbackQuery) -> bool:
        """Check if chat has permissible bot interaction level and required flags

        :param types.Message message: message which consists chat that should be checked
        :return bool: True if check is done successfully, else False
        """
        message = update if isinstance(
            update, types.Message) else update.message
        chat = get_chat_info(message.chat.id,
                             groups=self.chat_groups,
                             guilds=self.chat_guilds,
                             alliances=self.chat_alliances,
                             single_guild=self.chat_single_guild,
                             single_alliance=self.chat_single_alliance,
                             triggers_allowed=self.triggers_allowed)
        if chat is None:
            return False
        elif chat == 'multiple_guilds_found':
            await message.answer('Вы состоите больше, чем в одной гильдии. Для этого действия нужны точные сведения о конкретной гильдии. Попробуйте вызвать эту команду в нужном чате')
            return False
        elif chat == 'multiple_alliances_found':
            await message.answer('Вы состоите больше, чем в одном альянсе. Для этого действия нужны точные сведения о конкретном альянсе. Попробуйте вызвать эту команду в нужном чате')
            return False
        basic_alliance = captures.get(
            chat.alliance) if chat.alliance else chat.alliance
        cur_guild = guild.get(chat.guild) if chat.guild else chat.guild
        return {'chat': chat,
                'basic_alliance': basic_alliance,
                'guild': cur_guild}
