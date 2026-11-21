# Momentum

Telegram-бот о тренировках и сайт проекта.

- `bot/` — исходный код бота и материалы упражнений.
- `site/` — файлы сайта.

## Запуск бота

Нужны Python 3 и зависимости из `bot/requirements.txt`. В PowerShell из папки `bot`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Укажите токен Telegram-бота в локальном `.env`, затем запустите `python main.py`. Не публикуйте токен. База и список подписчиков создаются при использовании бота и не включены в репозиторий.

## Сайт

Откройте `site/index.html` в браузере.
