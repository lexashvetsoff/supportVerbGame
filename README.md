# supportVerbGame
Два бота-помошника - для telegram и vk для службы поддержки. Они закрывают все типичные вопросы, а вот что-то посложнее – перенаправляют на операторов.  

## Как настроить

Для запуска ботов вам понадобится Python третьей версии.  

Создайте файл .env с переменными окружения  

Затем установите зависимости

```sh
pip install -r requirements.txt
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом в корне проекта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны переменные:
- `TELEGRAM_BOT_TOKEN` — token телеграмм бота (получается у @BotFather при регистрации бота). 
- `PROJECT_ID` — id проекта на Google Cloud.
- `VK_TOKEN` - token vk бота (получается при создании группы в vk)
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу учетной записи службы, содержащий учетные данные закрытого ключа. Сохранить его нужно в формате `JSON` и положить в корень проекта. Более подробно о том как его получить можно посмотреть [здесь](https://stackoverflow.com/questions/43004904/accessing-gae-log-files-using-google-cloud-logging-python)

## Создание интентов (обучение ботов)
Обычение DialogFlow происходит через api. Для этого вам понадобится файл с вариантами вопросов от пользователей и ответом бота в формате `JSON`.  
Сам файл json должен иметь следующую структуру - пример:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
}
```

### Запуск
Чтобы сделать обучение необходимо запустить скрипт:
```sh
python3 create_intents.py
```

## Telegram бот

![Alt text](https://github.com/lexashvetsoff/supportVerbGame/blob/main/screen/demo_tg_bot.gif)  
[Пример рабочего бота](https://vk.com/public218494303)

### Запуск

```sh
python3 telegram_bot.py
```

## Vk бот

![Alt text](https://github.com/lexashvetsoff/supportVerbGame/blob/main/screen/demo_vk_bot.gif)  
Пример работы можно посмотреть написав в [группу в vk](https://t.me/verb_support_bot)

### Запуск

```sh
python3 telegram_bot.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).