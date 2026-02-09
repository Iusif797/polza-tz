# Как проверить, что всё работает

## 1. Проверка email-доменов

Реальные домены (gmail, yandex, mail.ru, outlook) + один заведомо несуществующий — чтобы увидеть все три типа статусов.

```bash
cd 1_email_verify
pip install -r requirements.txt
python email_verify.py --file emails_sample.txt
```

Или несколько адресов вручную:

```bash
python email_verify.py test@gmail.com info@yandex.ru user@nonexistent-xyz.invalid
```

Ожидаемо: для gmail.com, yandex.ru и т.п. — «домен валиден»; для nonexistent-xyz.invalid — «домен отсутствует». если у домена нет MX — «MX-записи отсутствуют или некорректны».

## 2. Отправка в Telegram

Токен и Chat ID — только свои (от @BotFather и getUpdates). Готовый текст уже в репозитории.

```bash
cd 2_telegram
export BOT_TOKEN=ваш_токен_от_BotFather
export CHAT_ID=ваш_chat_id_из_getUpdates
python send_telegram.py message_sample.txt
```

Успех: в чате появится текст из `message_sample.txt`. Ошибка: вывод в stderr, код выхода 1.

С .env (опционально):

```bash
pip install python-dotenv
cp config.example.env .env
# отредактировать .env — подставить BOT_TOKEN и CHAT_ID
python send_telegram.py message_sample.txt
```

## 3 и 4

Архитектура и блиц — документы. Открой `3_architecture/architecture.md` и `4_blitz/ai_stack.md`, при необходимости допиши ответы в блиц.
