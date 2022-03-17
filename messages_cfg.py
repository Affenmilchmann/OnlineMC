from cfg import prefix, DEFAULT_PORT

footer_text = {
    "en": f"OnlineMC | Found bug? Have a question? Use {prefix}help to see support server link",
    "ru": f"OnlineMC | Есть вопросы? Нашли баг? Ссылка на канал поддержки в {prefix}help"
}

help_links = {
    "en": ["**Get the plugin:**", "**Have a question? Found bug? Contact us here!**"],
    "ru": ["**Скачать плагин:**", "**Есть вопросы? Нашли баг? Свяжитесь с нами тут!**"]
}

lang_switched_msg = {
    "en": "**Swithed to english!**",
    "ru": "**Переключено на русский!**"
}

online_list_msg = {
    "server_offline": {
        "en": "Server is offline",
        "ru": "Сервер офлайн"
    },
    "server_empty": {
        "en": "Nobody is online!",
        "ru": "Никого нет в сети!"
    },
    "last_update": {
        "en": "*Last update: {}*",
        "ru": "*Обновлено: {}*"
    },
    "online_players": {
        "en": "**Online players:**",
        "ru": "**Игроки онлайн:**"
    },
}

command_descriptions = {
    "start": {
        "en": "Start! Call this command to start using bot",
        "ru": "Начать! Вызовите это команду для начала работы с ботом"
    },
    "create": {
        "en": "Creates online list updateable message in the channel where this command was recieved. This may take up to 10 seconds!",
        "ru": "Создать обновляемое сообщение со списком онлайн игроков в канале, где команда была вызвана. Это может занять до 10 секунд!"
    },
    "delete": {
        "en": "Deletes current online list updateable message",
        "ru": "Удалить текущее обновляемое сообщение со списком онлайн игроков"
    },
    "set_role": {
        "en": "Sets role that is able to manage bot settings. Warning! If no role was set, everbody will be able to change bot settings!",
        "ru": "Задать роль администратора, администраторы способны изменять настройки бота. Внимание! Если роль не задана, кто угодно может хоть поменять айпи, хоть удалить сообщение!"
    },
    "set_ip": {
        "en": "Sets minecraft server ip. Bot will request player data from there",
        "ru": "Задать айпи вашего майнкрафт сервера. Бот будет запрашивать оттуда список онлайн игроков"
    },
    "cfg": {
        "en": "Shows current bot's settings",
        "ru": "Показать текущие настройки"
    },
    "help": {
        "en": "Shows help message",
        "ru": "Показать сообщение-справку"
    },
    "ru": {
        "en": "Переключить язык бота на русский",
        "ru": "Переключить язык бота на русский"
    },
    "en": {
        "en": "Switch bot's language to english",
        "ru": "Switch bot's language to english"
    },
}

info_msgs = {
    "guild_inited": {
        "name": {
            "en": ["**Your server was linked!**", "*Friendly reminder:*"],
            "ru": ["**Ваш сервер успешно привязан!**", "*Важное напоминание:*"]
        },
        "value": {
            "en": [ "Before creating online player list message consider setting manager role and minecraft server ip.",
                   f"*This bot requires OnlineMC plugin running on the server. Link can be found in `{prefix}help`*"],
            "ru": [ "Прежде чем создавать сообщение со списком онлайн игроков убедитесь, что вы задали роль андинистратора и айпи майнкрафт сервера",
                   f"*Для работы этого бота вам необходимо установить плагин OnlineMC на сервер. Ссылка на плагин есть в `{prefix}help`*"]
        }
    },
    "guild_alr_inited": {
        "name": {
            "en": "**Oops!**",
            "ru": "**Упс!**"
        },
        "value": {
            "en": "Your server is already linked",
            "ru": "Ваш сервер уже и так привязан!"
        }
    },
    "guild_not_set_up": {
        "name": {
            "en": "**Server is not set up!**",
            "ru": "**Ваш сервер не настроен!**"
        },
        "value": {
            "en": f" - Use `{prefix}start` first. \n\
                     - Install OnlineMC plugin on your server (Link can be found in `{prefix}help`) \n\
                     - Make sure you set up your server's ip with `{prefix}set_ip`",
            "ru": f" - Сначала привяжите свой дискорд сервер с помощью `{prefix}start`. \n\
                     - Установите на ваш майнкрафт сервер плагин OnlineMC (Ссылка в `{prefix}help`) \n\
                     - Задайте айпи адрес своего майнкрафт сервера с помощью `{prefix}set_ip`"
        }
    },
    "guild_not_linked": {
        "name": {
            "en": "**Your discord server is not linked!**",
            "ru": "**Ваш дискорд сервер не привязан!**"
        },
        "value": {
            "en": f"Use `{prefix}start` first.",
            "ru": f"Сначала привяжите свой дискорд сервер с помощью `{prefix}start`."
        }
    },
    "cant_connect": {
        "name": {
            "en": "**Failed to connect to minecraft server**",
            "ru": "**Не удалось подключиться к майнкрафт серверу.**"
        },
        "value": {
            "en": f"Make sure you have\n \
                    - Installed OnlineMC plugin (Link can be found in `{prefix}help`)\n \
                    - Port {DEFAULT_PORT} opened on your server",
            "ru": f"Убедитесь, что вы\n \
                    - Установили плагин OnlineMC (Ссылка в `{prefix}help`)\n \
                    - Порт {DEFAULT_PORT} открыт в настройках вашего сервера"
        }
    },
    "invalid_syntax": {
        "en": "**Invalid syntax**",
        "ru": "**Неправильный синтаксис**"
    },
    "invalid_syntax_comments": {
        "ip_arg_missing": {
            "en": "`Ip` argument is missing",
            "ru": "Отсутствует аргумент `айпи`"
        },
        "role_arg_missing": {
            "en": "`Role` argument is missing",
            "ru": "Отсутствует аргумент `роль`"
        },
        "invalid_role": {
            "en": "Invalid role",
            "ru": "Несуществующая роль"
        }
    },
    "parameters": {
        "manager_role": {
            "en": "Manager role",
            "ru": "Роль администратора"
        },
        "ip": {
            "en": "Ip",
            "ru": "айпи"
        }
    },
    "unknown_command": {
        "name": {
            "en": "**Unknown command!**",
            "ru": "**Неизвестная комманда**"
        },
        "value": {
            "en": f"Try `{prefix}help`",
            "ru": f"Попробуйте `{prefix}help`"
        }
    },
    "not_permitted": {
        "en": "**You are not permitted to use this command!**",
        "ru": "**У вас нет прав использовать эту комманду!**"
    },
    "parameter_set": {
        "en": "`{name}` was set to {val}",
        "ru": "Параметру `{name}` было задано значение {val}"
    },
    "message_missing": {
        "name": {
            "en": "**Cant find online list message!**",
            "ru": "Не могу найти сообщение со списком онлайн игроков"
        },
        "value": {
            "en": "If message is present and you see this, delete online list message yourself",
            "ru": "Если вы это видите, но сообщение присутствует, удалите его вручную"
        }
    },
    "message_deleted": {
        "en": "**Message was deleted!**",
        "ru": "**Сообщение удалено!**"
    },
    "success": {
        "en": "**Success!**",
        "ru": "**Успех!**"
    },
}

cfg_msg = {
    "mgr_field_name": {
        "en": "**Manager role**",
        "ru": "**Роль администратора**"
    },
    "channel_field_name": {
        "en": "**Channel**",
        "ru": "**Канал**"
    },
    "msg_field_name": {
        "en": "**Online list message**",
        "ru": "**Сообщение с списком онлайн игроков**"
    },
    "ip_field_name": {
        "en": "**Server IP**",
        "ru": "**Айпи сервера**"
    },
    "missing_value": {
        "en": "Missing",
        "ru": "> Отсутствует"
    },
    "present_value": {
        "en": "Present",
        "ru": "> Присутствует"
    },
}
