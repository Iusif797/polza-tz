# 2. Отправка текста в Telegram

Скрипт читает содержимое .txt и отправляет его в выбранный приватный чат через Telegram-бота.

## Настройка

1. Создайте бота в Telegram: [@BotFather](https://t.me/BotFather) → /newbot → сохраните **токен**.
2. Узнайте **Chat ID** приватного чата: напишите боту в чат, откройте `https://api.telegram.org/bot<TOKEN>/getUpdates` и в ответе найдите `"chat":{"id": ...}`.
3. Скопируйте `config.example.env` в `.env` и подставьте значения:
   ```bash
   cp config.example.env .env
   ```
   Либо экспортируйте переменные:
   ```bash
   export BOT_TOKEN=...
   export CHAT_ID=...
   ```

Опционально для загрузки .env:
```bash
pip install python-dotenv
```

Без `python-dotenv` достаточно экспортировать `BOT_TOKEN` и `CHAT_ID` в окружении.

## Запуск

```bash
python send_telegram.py message.txt
```

С явным указанием токена и чата:
```bash
python send_telegram.py message.txt --token YOUR_TOKEN --chat YOUR_CHAT_ID
```

Python 3.8+.
