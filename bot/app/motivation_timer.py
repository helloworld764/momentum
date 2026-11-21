# import asyncio
# import datetime
# import random
# import logging
# from aiogram import Bot
# from app.subscription_store import get_subscribers
# import content.quotes as q
#
# logger = logging.getLogger(__name__)
#
# async def send_motivation_every_day(bot: Bot, hour: int = 23, minute: int = 8):
#     """Асинхронный цикл: ждём до следующего запуска, затем рассылаем."""
#     while True:
#         now = datetime.datetime.now()
#         next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
#         if next_run <= now:
#             next_run += datetime.timedelta(days=1)
#
#         wait_seconds = (next_run - now).total_seconds()
#         logger.info(f"[TIMER] Следующая отправка через {wait_seconds / 3600:.2f} часов")
#         await asyncio.sleep(wait_seconds)
#
#         # пересчёт времени перед отправкой
#         send_time = datetime.datetime.now()
#         # можно random.choice для случайного сообщения или по дате
#         message = random.choice(q.quotes)
#
#         subscribers = get_subscribers().copy()  # копируем чтобы избежать изменений во время итерации
#         if not subscribers:
#             logger.info("[TIMER] Нет подписчиков — ничего не отправляем.")
#             continue
#
#         for user_id in subscribers:
#             try:
#                 await bot.send_message(user_id, message)
#                 logger.info(f"[TIMER] Отправлено {user_id}")
#             except Exception as e:
#                 # Если чат заблокировал бота — можно удалить подписчика или логировать
#                 logger.exception(f"[TIMER] Ошибка при отправке {user_id}: {e}")
#                 # не удаляем автоматически, т.к. можно сначала проверить тип исключения


# m_timer.py


import asyncio
import datetime
import random
import logging
from aiogram import Bot
from app.subscription_store import get_subscribers
import content.quotes as q

logger = logging.getLogger(__name__)

MOTIVATION = q.quotes  # список цитат

def _is_time_equal(t1: str, t2: str) -> bool:
    """Сравнение времени в формате HH:MM — на случай лишних пробелов."""
    return t1.strip() == t2.strip()

async def send_motivation_every_day(bot: Bot):
    """Каждую минуту проверяем подписчиков и отправляем тем, у кого совпадает время."""
    while True:
        now_hm = datetime.datetime.now().strftime("%H:%M")
        subs = get_subscribers()

        # отладка: логируем тип и размер
        logger.debug(f"[TIMER] subscribers type={type(subs)}, count={len(subs) if hasattr(subs,'__len__') else 'unknown'}")

        # Если кто-то случайно сохранил список — проходим по нему
        if isinstance(subs, list):
            logger.warning("[TIMER] subscribers is a list — treating entries as user_ids (no time configured).")
            for uid in subs:
                try:
                    await bot.send_message(int(uid), random.choice(MOTIVATION))
                    logger.info(f"[TIMER] Отправлено {uid} (list mode)")
                except Exception as e:
                    logger.exception(f"[TIMER] Ошибка отправки {uid}: {e}")

            await asyncio.sleep(60)
            continue

        # Ожидается dict: user_id -> time_str (time_str может быть "")
        if isinstance(subs, dict):
            for user_id, user_time in subs.items():
                # Пропускаем пользователей без настроенного времени
                if not user_time:
                    continue
                try:
                    if _is_time_equal(user_time, now_hm):
                        await bot.send_message(int(user_id), random.choice(MOTIVATION))
                        logger.info(f"[TIMER] Отправлено {user_id} в {now_hm}")
                except ValueError:
                    logger.exception(f"[TIMER] Невалидный user_id: {user_id}")
                except Exception as e:
                    logger.exception(f"[TIMER] Ошибка отправки {user_id}: {e}")
        else:
            logger.error(f"[TIMER] Unexpected subscribers type: {type(subs)}. Content: {subs}")

        await asyncio.sleep(60)