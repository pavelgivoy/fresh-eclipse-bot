settings_translating = {
    "locations_review_allowed": "Ответ на форварды из бота о локациях и альянсах",
    "withdrawing_allowed": "Генерация ссылок на сдачу и выдачу ресурсов",
    "triggers_allowed": "Создание, изменение, удаление и использование триггеров",
}

settings_translating_reversed = {v: k for k, v in settings_translating.items()}

status_from_bool = {
    True: "Разрешено",
    False: "Запрещено",
}

status_from_key = {v: k for k, v in status_from_bool.items()}
