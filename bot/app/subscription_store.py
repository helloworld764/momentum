# import json
# from pathlib import Path
# from typing import Set
#
#
# STORE_PATH = Path("content/subscribers.json")
#
#
# def _load() -> Set[int]:
#     if not STORE_PATH.exists():
#         return set()
#     try:
#         data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
#         return set(int(x) for x in data)
#     except Exception:
#         return set()
#
#
# def _save(subs: Set[int]):
#     STORE_PATH.write_text(json.dumps(list(subs)), encoding="utf-8")
#
#
# _subscribers = _load()
#
#
# def get_subscribers() -> Set[int]:
#     return _subscribers
#
#
# def add_subscriber(user_id: int) -> bool:
#     """Return True if added (new), False if already present."""
#     if user_id in _subscribers:
#         return False
#     _subscribers.add(int(user_id))
#     _save(_subscribers)
#     return True
#
#
# def remove_subscriber(user_id: int) -> bool:
#     if user_id in _subscribers:
#         _subscribers.remove(int(user_id))
#         _save(_subscribers)
#         return True
#     return False

# app/subscription_store.py

import json
from pathlib import Path
from typing import Dict, Union

FILE = Path("content/subscribers.json")

def _load_raw():
    if not FILE.exists():
        return {}
    try:
        return json.loads(FILE.read_text("utf-8"))
    except Exception:
        return {}

def _save_raw(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# Внутренное представление — всегда словарь str(user_id) -> "HH:MM"
_subscribers: Dict[str, str] = {}

# Загружаем при импорте и нормализуем данные
_raw = _load_raw()
if isinstance(_raw, dict):
    # возможна ситуация, когда значения не строки -> приводим к строкам
    for k, v in _raw.items():
        try:
            _subscribers[str(int(k))] = str(v)
        except Exception:
            # если ключ не приводится к int — пропускаем
            continue
elif isinstance(_raw, list):
    # старый формат — просто список user_id (без времени). Подставим None/пустую строку.
    for uid in _raw:
        try:
            _subscribers[str(int(uid))] = ""  # пустое время — пользователь есть, но время не установлено
        except Exception:
            continue
else:
    # неожиданный формат — игнорируем
    _subscribers = {}

def save():
    """Сохранить текущее состояние в файл."""
    _save_raw(_subscribers)

def set_user_time(user_id: int, time_str: str):
    _subscribers[str(int(user_id))] = time_str
    save()

def remove_user(user_id: int):
    _subscribers.pop(str(int(user_id)), None)
    save()

def get_subscribers() -> Dict[str, str]:
    """Вернёт словарь str(user_id) -> time_str (может быть пустая строка)."""
    return _subscribers