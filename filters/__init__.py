from aiogram import Dispatcher

from .chat_filter import ChatFilter
from .chat_member_update_filter import ChatMemberUpdateFilter
from .forward_filter import ForwardFilter
from .is_battle_order import IsBattleOrder
from .is_guild_roster import IsGuildRoster
from .is_guild_stats import IsGuildStats
from .is_guru_profile import IsGuruProfile
from .user_filter import UserFilter
from .user_is_admin_of_input_chat import UserIsAdminOfInputChat
from .trigger_filter import TriggerFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(ChatFilter)
    dp.filters_factory.bind(ChatMemberUpdateFilter, event_handlers=[
        dp.chat_member_handlers, dp.my_chat_member_handlers])
    dp.filters_factory.bind(ForwardFilter, event_handlers=[
                            dp.message_handlers])
    dp.filters_factory.bind(IsBattleOrder, event_handlers=[
                            dp.message_handlers])
    dp.filters_factory.bind(IsGuildRoster, event_handlers=[
                            dp.message_handlers])
    dp.filters_factory.bind(IsGuildStats, event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(IsGuruProfile, event_handlers=[
                            dp.message_handlers])
    dp.filters_factory.bind(UserFilter)
    dp.filters_factory.bind(UserIsAdminOfInputChat)
    dp.filters_factory.bind(TriggerFilter, event_handlers=[
                            dp.message_handlers])
