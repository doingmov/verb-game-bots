# Боты поддержки «Игра глаголов»

Проект для онлайн-издательства «Игра глаголов»: два чат-бота службы поддержки
(Telegram и ВКонтакте), которые отвечают на типовые вопросы клиентов с помощью
нейросети и не мешают операторам, если не понимают вопрос.

## Что такое Dialogflow

[Dialogflow](https://cloud.google.com/dialogflow) — сервис Google для создания
диалоговых интерфейсов. Разработчик описывает намерения пользователя (Intents)
через примеры фраз, а Dialogflow сам распознаёт похожие формулировки и
возвращает заранее заданный ответ. Это позволяет боту понимать вопросы,
сформулированные разными словами, без написания правил вручную.

## Как это работает

- Пользователь пишет боту в Telegram или ВКонтакте.
- Бот пересылает текст в Dialogflow через API.
- Dialogflow определяет намерение и возвращает готовый ответ.
- Если вопрос непонятен (сработал Fallback Intent):
  - в Telegram бот отвечает стандартной фразой Dialogflow;
  - в ВКонтакте бот молчит, чтобы не мешать оператору поддержки.
- Если бот падает или получает неожиданную ошибку, сообщение об этом
  автоматически приходит разработчику в отдельный Telegram-чат.

## Попробовать ботов

- Telegram: [Мой telegram bot](https://t.me/verb_gamee_support_bot)
- ВКонтакте: [Мое сообщество вк]https://vk.ru/club241646134

## Как запустить локально

```bash
git clone https://github.com/doingmov/verb-game-bots.git
cd verb-game-bots
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните переменные:

- `TELEGRAM_BOT_TOKEN` — токен бота, полученный у [@BotFather](https://t.me/BotFather)
- `VK_GROUP_TOKEN` — токен доступа сообщества ВКонтакте
- `DIALOGFLOW_PROJECT_ID` — Project ID агента Dialogflow
- `GOOGLE_APPLICATION_CREDENTIALS` — путь к файлу ключей Google Cloud
- `LOGS_BOT_TOKEN`, `LOGS_CHAT_ID` — бот и чат для уведомлений об ошибках

Запуск:

```bash
python tg_bot.py
python vk_bot.py
```

## Создание интентов из файла

Тренировочные фразы и ответы для Dialogflow загружаются скриптом:

```bash
python create_intents.py questions.json
```

## Деплой

Боты развёрнуты на сервере и работают постоянно через `systemd`
(`tg_bot.service`, `vk_bot.service`), автоматически перезапускаясь при сбоях.
