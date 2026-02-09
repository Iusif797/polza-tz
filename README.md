# Polza Outreach Engine — тестовое задание

Репозиторий содержит решение тестового задания: скрипты проверки email и интеграции с Telegram, архитектурный документ и ответы на блиц.

---

## Структура проекта

| № | Задание | Содержимое |
|---|---------|------------|
| 1 | Проверка email-доменов | Скрипт: MX-записи + SMTP handshake (без отправки письма). Один `.py`, инструкция в папке. |
| 2 | Интеграция с Telegram | Скрипт: чтение текста из `.txt` → отправка в приватный чат через бота. |
| 3 | Архитектура | Документ: 1200 email для аутрича — сервисы, ротация, мониторинг, риски, стоимость. |
| 4 | Блиц | Ответы: IDE, модели, MCP, cursor rules. |

---

## Быстрый старт

**Часть 1 — проверка email**
```bash
cd 1_email_verify
pip install -r requirements.txt
python email_verify.py --file emails_sample.txt
```

**Часть 2 — Telegram**
```bash
cd 2_telegram
# Заполнить .env из config.example.env (BOT_TOKEN, CHAT_ID)
pip install python-dotenv
python send_telegram.py message_sample.txt
```

Подробные шаги и зависимости — в `README.md` внутри каждой папки.

---

## Ссылки на разделы

- [1_email_verify](1_email_verify/) — проверка email
- [2_telegram](2_telegram/) — отправка в Telegram
- [3_architecture/architecture.md](3_architecture/architecture.md) — архитектура
- [4_blitz/ai_stack.md](4_blitz/ai_stack.md) — AI-стек

---

