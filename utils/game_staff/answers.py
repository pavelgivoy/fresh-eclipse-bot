# common
ERROR_HAPPENED_DEV = 'При попытке {} произошла ошибка.'
ERROR_HAPPENED_USER = 'Что-то пошло не так.'
NOT_ENOUGH_INFO = 'Не хватает информации'
SEE_LOGS = 'Подрбоности в логах'
THANKS = 'Спасибо!'

# handlers common
PROVIDE_ACTUAL_FORWARD = 'Я хочу видеть самую свежую информацию! (Не старше {})'

# captures
ADD_CAPTURE_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'добавить новую локацию') + ' ' + SEE_LOGS
ADD_CAPTURE_ERROR_USER = ERROR_HAPPENED_USER + ' ' + 'Локация не добавлена'
ALLIANCE_ACTIVE = 'Альянс <b>{}</b> активен'
ALLIANCE_DEACTIVATED = 'Альянс <b>{}</b> неактивен'
ALLIANCE_UPDATE_STATUS_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'изменить статус альянса <b>{}</b> (<code>{}</code>)') + ' ' + SEE_LOGS
ALLIANCE_UPDATE_STATUS_ERROR_USER = ERROR_HAPPENED_USER + \
    ' ' + 'Статус альянса не изменён'
BATTLE_FOUND = 'Эта битва уже была записана'
BATTLE_REPORT_ERROR = ERROR_HAPPENED_DEV.format(
    'записать результаты данной битвы') + ' ' + SEE_LOGS
CLEAR_ALL_LOCATIONS_DONE = 'Список локаций очищен'
CLEAR_ALL_LOCATIONS_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'очистить список локаций и их истории') + ' ' + SEE_LOGS
CLEAR_ALL_LOCATIONS_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Список локаций не был очищен'
DELETE_LOCATION_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'удалить локацию и её историю') + ' ' + SEE_LOGS
DELETE_LOCATION_ERROR_USER = ERROR_HAPPENED_USER + ' Локация не удалена'
FORCE_UPDATE_OWNER_DONE = 'Сведения о текущем владельце изменены. ' + THANKS
FORCE_UPDATE_OWNER_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'изменить владельца локации') + ' ' + SEE_LOGS
FORCE_UPDATE_OWNER_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Сведения о владельце не изменены'
FORCE_UPDATE_OWNER_WRONG_ARGS = 'Неправильно указаны аргументы. Сначала укажите код локации, затем имя нового владельца'
GO_DEF_CAPTURE = 'Какая атака? Иди дефать!\n'
HISTORY_NOT_FOUND = 'У этой локации нет истории. Изменить владельца невозможно'
KNOWN_CAPTURE = 'Локация уже известна'
NEW_CAPTURE = 'Новая локация!\n<b>{}</b>\n<code>{}</code>'
LOCATION_ADDED = 'Локация добавлена. ' + THANKS
LOCATION_DELETED = 'Локация <b>{}</b> (<code>{}</code>) удалена.'
LOCATION_IS_OWNER_FORBIDDEN = 'Владельцем может стать только альянс'
NOT_ENOUGH_CAPTURE_MANUAL_ADD_INFO = NOT_ENOUGH_INFO + 'об имени или локации'
CAPTURE_SET_OWNER_WARNING_PATTERN = 'Возможно, это{}ваша локация. Но, если вы очень хотите её {}, то держите команду:'
OWN_CAPTURE_WARNING = CAPTURE_SET_OWNER_WARNING_PATTERN.format(
    ' ', 'атаковать')
NOT_OWN_CAPTURE_WARNING = CAPTURE_SET_OWNER_WARNING_PATTERN.format(
    ' не ', 'защищать')
UNKNOWN_CAPTURE = 'Нет информации о точке с кодом <code>{}</code>'
UNKNOWN_OWNER = 'Нет альянса с именем <b>{}</b>'
UNKNOWN_BUFF_TYPE_OR_PRICE = 'Информация о бафах точки <b>{}</b> не записана, поскольку не определены цена или тип бафа'
DELETE_RESOURCE_INFO_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'удалить информацию о ресурсах точки <b>{}</b>') + ' ' + SEE_LOGS
DELETE_RESOURCE_INFO_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Инорфмация о точке {} не удалена'
DELETE_RESOURCE_INFO_DONE = 'Информация о бафах и ресурсах точки удалена'
UPDATE_RESOURCE_INFO_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'изменить информацию о ресурсах точки <b>{}</b>') + ' ' + SEE_LOGS
UPDATE_RESOURCE_INFO_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Информация о точке {} не записана'
UPDATE_RESOURCE_INFO_DONE = 'Информация о бафах и ресурсах точки записана'

# chats
BROADCAST_ERROR = ERROR_HAPPENED_DEV.format(
    'отправить сообщение в чат с id <code>{}</code>') + '\n{}'
BROADCAST_DONE = 'Сообщение отправлено в чаты'
CHAT_ADDED = 'Новый чат добавлен'
CHAT_NOT_ADDED = 'Чат не добавлен'
CHAT_DELETED = 'Чат удалён'
CHAT_NOT_DELETED = 'Чат не удалён'
NO_CHAT_ID = 'Нет id чата'
CHAT_ADDING_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'добавить новый чат в БД') + ' ' + SEE_LOGS
CHAT_DELETING_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'удалить чат из БД') + ' ' + SEE_LOGS
CHAT_ID_INPUT_IS_NOT_ALLOWED = (
    'Вам нельзя указывать чат с помощью ручного ввода.'
    'В следующем сообщении будут указаны настройки чата, в котором вызвана команда.'
    'Для исправления настроек другого чата вызовите команду прямо в нём'
)
CHAT_KNOWN = 'Чат с id <code>{}</code> уже известен'
CHAT_SETTINGS_CHANGED = 'Настройки чата с id <code>{}</code> успешно изменены'
CHAT_SETTINGS_CHANGING_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'изменить настройки чата с id <code>{}</code>') + ' ' + SEE_LOGS
CHAT_SETTING_CHANGING_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Настройки чата не изменены'
CHAT_SETTING_CHANGING_NOT_ALLOWED = 'Вам нельзя менять настройки чата с id <code>{}</code>'
CHAT_UNKNOWN = 'Чат с id <code>{}</code> неизвестен'
BOT_LEFT_THE_CHAT = 'Бот больше не состоит в чате с id <code>{}</code>.Чат и связанные с ним данные удалены из БД'
UNKNOWN_CHAT_WARNING_DEV = 'Бота добавили в неизвестный чат с id: <code>{}</code>, но он оттуда уже вышел'
UNKNOWN_CHAT_WARNING_USER = '👀 new chat with id: <code>{}</code>'
GUILD_MARKED = 'Твоя гильдия уже отметилась'
ALL_GUILDS_MARKED = 'Все отметились, всем по грибочку 🍄'

# guilds
GUILD_ADD_MANUALLY_NO_ARGS = 'Нет информации о гильдии, или она неполная (должны быть тэг, замок и имя)'
GUILD_KNOWN = 'Гильдия <b>{}</b> уже известна'
GUILD_UNKNOWN = 'Гильдия <b>{}</b> неизвестна'
GUILD_IN_BASIC_ALLIANCE = 'Гильдия <b>{}</b> {} состоит в альянсе <b>{}</b>'
GUILD_DELETE_MANUALLY_NO_ARGS = 'Нужно передать тэг гильдии'
GUILD_DELETE_MANUALLY_ERROR = ERROR_HAPPENED_DEV.format(
    'удалить гильдию <b>{}</b>') + ' ' + SEE_LOGS
GUILDS_ALLIANCE_NOT_FOUND = 'Не удалось найти информацию об альянсе этих гильдий'
GUILDS_ALLIANCE_UPDATE_INFO_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'изменить информацию о составе альянса<b>{}</b>') + ' ' + SEE_LOGS
GUILDS_ALLIANCE_UPDATE_INFO_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Информация о составе альянса <b>{}</b> не изменена'
GUILDS_ALLIANCE_UPDATE_INFO_DONE = 'Инфомация о составе альянса <b>{}</b> изменена. ' + THANKS
GUILD_INFO_UPDATE_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'изменить информацию о гильдии <b>{}</b>') + ' ' + SEE_LOGS
GUILD_INFO_UPDATE_ERROR_USER = ERROR_HAPPENED_USER + \
    ' Информация о гильдии не изменена'
GUILD_INFO_UPDATE_DONE = 'Информация о гильдии <b>{}</b> изменена. ' + THANKS
OMITED_GUILDS_WARNING = (
    'Этих гильдий нет в нашем альянсе: <b>{}</b>\n'
    'Их данные не будут указаны'
)
GUILD_ROSTER_UPDATE_DONE = 'Состав <b>{}</b> обновлён. ' + THANKS
GUILD_STATS_UPDATE_DONE = 'Ура! Теперь я имею свежую информацию о силе твоей гильдии. ' + THANKS


# requests
REQUEST_ID_REQUIRED = 'Возможно, вы забыли указать номер хотелки'
REQUEST_ID_OR_TEXT_REQUIRED = 'Укажите номер хотелки и измененный текст'
REQUEST_NOT_DEFINED = 'А что же вы хотите?'
REQUEST_FOUND = 'Такая хотелка уже есть'
REQUEST_NOT_FOUND = 'Эта хотелка не найдена'
REQUEST_ADDED = 'Хотелка добавлена'
REQUEST_DELETED = 'Эта хотелка удалена'

# users
USER_INFO_REQUIRED = 'Не хватает сведений о гильдии, id юзера или его юзернейма'
USER_IS_REPR = '<code>{}</code> уже является представителем гильдии <b>{}</b>'
ADD_REPR_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'добавить представителя гильдии <b>{}</b>') + ' ' + SEE_LOGS
ADD_REPR_DONE = 'Теперь у гильдии <b>{}</b> новый представитель: <code>{}</code>'
UNKNOWN_FLAG_WARNING = 'Недопустимый параметр <code>{}</code>. Он будет пропущен'
UNKNOWN_REPR = 'Я не знаю, кто это... {}'
USER_IS_NOT_REPR = 'Юзер {} <code>{}</code> не является представителем гильдии <b>{}</b>'
DELETE_REPR_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'удалить представителя гильдии <b>{}</b>') + ' ' + SEE_LOGS
DELETE_REPR_DONE = 'Юзер {} <code>{}</code> больше не является представителем гильдии <b>{}</b>'
USER_ID_REQUIRED = 'Необходимы сведения об id пользователя'
USER_MEMBER_INFO_UPDATE_FAILED = 'Информация о пользователе не получена'
USER_IS_NOT_A_MEMBER_OF_CHAT = 'Пользователь с id <code>{}</code> не состоит в чате с id <code>{}</code>'
ADD_USER_AND_CHAT_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'добавить нового прдеставителя чата с id <code>{}</code>') + ' ' + SEE_LOGS
ADD_USER_AND_CHAT_ERROR_USER = 'Юзер не добавлен'
ADD_USER_AND_CHAT_DONE = 'Ок!'
ADD_USER_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'добавить пользователя с id {} в БД') + ' ' + SEE_LOGS


# gurus
SEND_GURU_PROFILE = 'Пришлите профиль кузнеца и/или алхимика из бота'
SEND_GURU_USERNAME = 'Укажите юзернейм мастера'
WRONG_SHOP_LINK = 'Неправильная ссылка на лавку'
GURU_NOT_FOUND = 'Лавка не найдена'
GURU_DELETED = 'Лавка этого мастера удалена'
SELECT_GURU_SPEC_LEVEL = 'Каков уровень навыка для специализации <b>{}</b>?'
GURU_UPDATED = 'Информация о лавке обновлена. ' + THANKS
GURU_UPDATE_ERROR_DEV = ERROR_HAPPENED_DEV.format(
    'обновить информацию о лавке') + ' ' + SEE_LOGS
GURU_UPDATE_ERROR_USER = ERROR_HAPPENED_USER + ' Лавка не записана'


# triggers
TRIGGER_NAME_REQUIRED = 'Укажите название триггера'
TRIGGER_ADDED = 'Триггер добавлен'
TRIGGER_DELETED = 'Триггер удалён'
TRIGGER_EDIT_DENIED = 'Вам нельзя изменять этот триггер'
TRIGGER_NOT_FOUND = 'Но такого триггера нет'
TRIGGER_PARSE_FAILED = 'Не найдено значение триггера (текст, фото, видео, стикер, войс, кружок и т.д.)'
