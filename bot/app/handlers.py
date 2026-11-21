from aiogram import F, Router, Bot, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BotCommand, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from typing import Optional, Tuple
import datetime
import aiosqlite
import asyncio


import app.keyboards as kb
import content.exercises as ex
from app.subscription_store import set_user_time, remove_user, get_subscribers
from content.partners import partner


router = Router()


class UserTime(StatesGroup):
    waiting_for_time = State()

class Reg(StatesGroup):
    name_reg = State()
    height_reg = State()
    weight_reg = State()

class OneRepMax(StatesGroup):
    weight_1RM = State()
    repetitions_1RM = State()


user_exercises_state = {}


exercisesCount = 0
exercises_d1 = [ex.exercise1_d1, ex.exercise2_d1, ex.exercise3_d1, ex.exercise4_d1, ex.exercise5_d1]
exercises_d2 = [ex.exercise1_d2, ex.exercise2_d2, ex.exercise3_d2, ex.exercise4_d2, ex.exercise5_d2]
exercises_d3 = [ex.exercise1_d3, ex.exercise2_d3, ex.exercise3_d3, ex.exercise4_d3, ex.exercise5_d3]


BOT_COMMANDS = [
    BotCommand(command="start", description="🏋️‍♂️ Запустить бота"),
    BotCommand(command="help", description="❓ Помощь"),
]


async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands(BOT_COMMANDS)

@router.startup()
async def on_startup(bot: Bot):
    await setup_bot_commands(bot)
    print("✅ Команды бота установлены")

### БД
async def add_user_to_database(telegram_id, username):
    async with aiosqlite.connect('coach_bot.db') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (telegram_id BEGINT, username TEXT, date TEXT)")
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?",  (telegram_id,))
        data = await cursor.fetchone()
        if data is not None:
            print('none coach_bot.db - users')
            return
    date = f'{datetime.date.today()}'
    async with aiosqlite.connect('coach_bot.db') as db:
        await db.execute("INSERT INTO users (telegram_id, username, date) VALUES (?, ?, ?)", (telegram_id, username, date))
        await db.commit()

async def add_athletes_to_database(telegram_id, name, height, weight):
    async with aiosqlite.connect('coach_bot.db') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS athletes (telegram_id BEGINT, name TEXT, height INTEGER, weight INTEGER)")
        cursor = await db.execute("SELECT * FROM athletes WHERE telegram_id = ?", (telegram_id,))
        data = await cursor.fetchone()
        if data is not None:
            print('none coach_bot.db - athletes')
            return
    async with aiosqlite.connect('coach_bot.db') as db:
        await db.execute("INSERT INTO athletes (telegram_id, name, height, weight) VALUES (?, ?, ?, ?)", (telegram_id, name, height, weight))
        await db.commit()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(photo=FSInputFile('media/start_picture.jpg'),
                        caption='<b>Привет, спортсмен!</b> 💪\n\nТы попал в зону создания лучшей версии себя, и мы начинаем великое преображение!\n\n'
                         '📍 Готов стать сильнее, выносливее и увереннее?\n'
                         '📍 Хочешь чувствовать себя машиной после каждой тренировки?\n'
                         '📍 Мечтаешь о теле, которое работает на тебя 24/7?\n\n'
                         'Вместе мы превратим "Я не могу" в "Я сделал это!"\n''Каждая капля пота - это шаг к твоему успеху! ✊',
                         reply_markup=kb.start)
    telegram_id = message.from_user.id
    username = message.from_user.username
    await add_user_to_database(telegram_id, username)


@router.callback_query(F.data == 'backward_to_menu')
async def backward_to_menu(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer_photo(photo=FSInputFile('media/start_picture.jpg'),
                        caption='<b>Привет, спортсмен!</b> 💪\n\nТы попал в зону создания лучшей версии себя, и мы начинаем великое преображение!\n\n'
                         '📍 Готов стать сильнее, выносливее и увереннее?\n'
                         '📍 Хочешь чувствовать себя машиной после каждой тренировки?\n'
                         '📍 Мечтаешь о теле, которое работает на тебя 24/7?\n\n'
                         'Вместе мы превратим "Я не могу" в "Я сделал это!"\n''Каждая капля пота - это шаг к твоему успеху! ✊',
                         reply_markup=kb.start)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('❓ <b>Помощь в использовании бота и техподдержка.</b>\n\n'
                         '<b>Команды бота:</b>\n'
                         '/start — запустить бота\n'
                         '/help — помощь\n'
                         '/info — посмотреть информацию о боте\n'
                         '/profile — открыть профиль\n'
                         '/settings — открыть настройки\n'
                         '/reg — зарегистрироваться\n'
                         '/start_motivation — включить ежедневную мотивацию\n'
                         '/stop_motivation — выключить ежедневную мотивацию\n\n'
                         '💬 Если возникла проблема c ботом, напишите сюда: @iisssslaam.\n'
                         '💬 Если возник вопрос об упражнениях, напишите сюда: @SiZank.',
                         parse_mode='HTML')


@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer_sticker(sticker='CAACAgIAAxkBAAIIcWlIYecooj7xEvGg2ynS3WNpStpYAAJflgACO7xASqvymyiV35lpNgQ')
    await message.answer('<b>Momentum Bot</b> — это бот для тренировок, созданный студентами 1го курса КНИТУ-ИХТИ, группы 151-24.\n\n'
                         'При помощи него вы можете начать заниматься в зале и привести себя в форму. Бот рассчитан как на новичков,'
                         ' так и на более опытных спортсменов.\n\n'
                         'Приятного использования!\n\n'
                         '<b>Software Developer:</b> @iisssslaam\n'
                         '<b>Content Manager:</b> @SiZank\n')


# start/ stop motivation
@router.message(Command("start_motivation"))
async def cmd_start_motivation(message: Message):
    user_id = message.from_user.id
    subs = get_subscribers()
    if str(user_id) in subs and subs[str(user_id)]:
        return await message.answer("🔔 Рассылка уже включена. Время: " + subs[str(user_id)])
    # Если пользователя нет — он должен выбрать время
    await message.answer(
        "Чтобы включить рассылку, введите время в которое желаете получать сообщения:",
        reply_markup=kb.set_time
    )

@router.message(Command("stop_motivation"))
async def cmd_stop_motivation(message: Message):
    user_id = message.from_user.id
    remove_user(user_id)
    await message.answer("❌ Ты отписался от рассылки. В любой момент можно подписаться снова в настройках или командой /start_motivation")


# Начать тренировку --> уровень --> упражнения
@router.callback_query(F.data == 'startTraning')
async def startTraning(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer('Наш метод тренировок выстроен относительно недели, поэтому далее вам будет предложено'
                                  ' выбрать какой это у вас по счету день тренировки за неделю.'
                                  ' (более подробную информацию о тренировочном процессе можете почитать на нашем сайте)\n\n'
                                  '<i>Примечание: вы можете тренироваться в любые дни недели с отдыхом в один день '
                                  '(например: пн, ср, пт или вт, чт, сб).</i>',
                                  reply_markup=kb.continue_backward_to_menu, parse_mode='HTML')

@router.callback_query(F.data == 'continue_to_days')
async def continue_to_days(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('🗓️ <b>Выберите день тренировки (в неделе):</b>', reply_markup=kb.days, parse_mode='HTML')

@router.callback_query(F.data == 'backward_to_continue')
async def backward_to_continue(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Наш метод тренировок выстроен относительно недели, поэтому далее вам будет предложено'
                                  ' выбрать какой это у вас по счету день тренировки за неделю.'
                                  ' (более подробную информацию о тренировочном процессе можете почитать на нашем сайте)\n\n'
                                  '<i>Примечание: вы можете тренироваться в любые дни недели с отдыхом в один день '
                                  '(например: пн, ср, пт или вт, чт, сб).</i>',
                                  reply_markup=kb.continue_backward_to_menu, parse_mode='HTML')


### НАЧАЛЬНЫЙ УРОВЕНЬ
@router.callback_query(F.data == 'first_day')
async def first_day(callback: CallbackQuery):

    await callback.answer('Вы выбрали день 1')

    user_id = callback.from_user.id
    user_exercises_state[user_id] = {
        "count": 0,
        "level": "l1"
    }

    await callback.message.edit_media(media=exercises_d1[0], reply_markup=kb.forward_backwardToDays_d1)


@router.callback_query(F.data == 'forward_d1')
async def forward_d1(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 0, "level": "l1"}

    state = user_exercises_state[user_id]
    current_count = state["count"]

    new_count = (current_count + 1) % 5

    user_exercises_state[user_id]["count"] = new_count

    if new_count == 4:
        reply_markup = kb.forwardToLast_backward_d1
    elif new_count == 0:
        reply_markup = kb.forward_backwardToDays_d1
    else:
        reply_markup = kb.forward_backward_d1

    try:
        await callback.message.edit_media(media=exercises_d1[new_count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.edit_media(media=exercises_d1[new_count], reply_markup=reply_markup)


@router.callback_query(F.data == 'backward_d1')
async def backward_d1(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 0, "level": "l1"}

    state = user_exercises_state[user_id]
    current_count = state["count"]

    new_count = (current_count - 1) % 5

    user_exercises_state[user_id]["count"] = new_count

    if new_count > 0:
        reply_markup = kb.forward_backward_d1
    else:
        reply_markup = kb.forward_backwardToDays_d1

    await callback.message.edit_media(media=exercises_d1[new_count], reply_markup=reply_markup)


@router.callback_query(F.data == 'backward_to_days_d1')
async def backward_to_days_d1(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id in user_exercises_state:
        del user_exercises_state[user_id]

    await callback.message.delete()
    await callback.message.answer('🗓️ <b>Выберите день тренировки (в неделе):</b>', reply_markup=kb.days, parse_mode='HTML')


@router.callback_query(F.data == 'forward_to_last_d1')
async def forward_to_last_d1(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 4, "level": "l1"}
    else:
        user_exercises_state[user_id]["count"] = 4

    await callback.message.delete()
    await callback.message.answer(text=ex.programForTraining_l1, reply_markup=kb.backwardToExercises_d1)


@router.callback_query(F.data == 'backward_to_exercises_d1')
async def backward_to_exercises_d1(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 4, "level": "l1"}

    state = user_exercises_state[user_id]
    count = state["count"]

    if count == 4:
        reply_markup = kb.forwardToLast_backward_d1
    elif count == 0:
        reply_markup = kb.forward_backwardToDays_d1
    else:
        reply_markup = kb.forward_backward_d1

    await callback.message.edit_media(media=exercises_d1[count], reply_markup=reply_markup)


### СРЕДНИЙ УРОВЕНЬ
@router.callback_query(F.data == 'second_day')
async def second_day(callback: CallbackQuery):
    await callback.answer('Вы выбрали день 2')

    user_id = callback.from_user.id
    user_exercises_state[user_id] = {
        "count": 0,
        "level": "l2",
        "current_level": "l2"
    }

    await callback.message.edit_media(media=exercises_d2[0], reply_markup=kb.forward_backwardToDays_d2)


@router.callback_query(F.data == 'forward_d2')
async def forward_d2(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 0, "level": "l2", "current_level": "l2"}

    state = user_exercises_state[user_id]
    current_count = state["count"]

    new_count = (current_count + 1) % 5

    user_exercises_state[user_id]["count"] = new_count

    if new_count == 4:
        reply_markup = kb.forwardToLast_backward_d2
    elif new_count == 0:
        reply_markup = kb.forward_backwardToDays_d2
    else:
        reply_markup = kb.forward_backward_d2

    try:
        await callback.message.edit_media(media=exercises_d2[new_count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.delete()
        await callback.message.edit_media(media=exercises_d2[new_count], reply_markup=reply_markup)


@router.callback_query(F.data == 'backward_d2')
async def backward_d2(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 0, "level": "l2", "current_level": "l2"}

    state = user_exercises_state[user_id]
    current_count = state["count"]

    new_count = (current_count - 1) % 5

    user_exercises_state[user_id]["count"] = new_count

    if new_count > 0:
        reply_markup = kb.forward_backward_d2
    else:
        reply_markup = kb.forward_backwardToDays_d2

    try:
        await callback.message.edit_media(media=exercises_d2[new_count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.delete()
        await callback.message.edit_media(media=exercises_d2[new_count], reply_markup=reply_markup)


@router.callback_query(F.data == 'backward_to_days_d2')
async def backward_to_days_d2(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id in user_exercises_state:
        del user_exercises_state[user_id]

    await callback.message.delete()
    await callback.message.answer('🗓️ <b>Выберите день тренировки (в неделе):</b>', reply_markup=kb.days, parse_mode='HTML')


@router.callback_query(F.data == 'forward_to_last_d2')
async def forward_to_last_d2(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 4, "level": "l2", "current_level": "l2"}
    else:
        user_exercises_state[user_id]["count"] = 4

    await callback.message.delete()
    await callback.message.answer(text=ex.programForTraining_l2, reply_markup=kb.backwardToExercises_d2)


@router.callback_query(F.data == 'backward_to_exercises_d2')
async def backward_to_exercises_d2(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 4, "level": "l2", "current_level": "l2"}

    state = user_exercises_state[user_id]
    count = state["count"]

    if count == 4:
        reply_markup = kb.forwardToLast_backward_d2
    elif count == 0:
        reply_markup = kb.forward_backwardToDays_d2
    else:
        reply_markup = kb.forward_backward_d2

    try:
        await callback.message.edit_media(media=exercises_d2[count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.delete()
        await callback.message.edit_media(media=exercises_d2[count], reply_markup=reply_markup)


### ПРОДВИНУТЫЙ УРОВЕНЬ
@router.callback_query(F.data == 'third_day')
async def third_day(callback: CallbackQuery):
    await callback.answer('Вы выбрали день 3')

    user_id = callback.from_user.id
    user_exercises_state[user_id] = {
        "count": 0,
        "level": "l3",
        "current_level": "l3"
    }

    await callback.message.edit_media(media=exercises_d3[0], reply_markup=kb.forward_backwardToDays_d3)


@router.callback_query(F.data == 'forward_d3')
async def forward_d3(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 0, "level": "l3", "current_level": "l3"}

    state = user_exercises_state[user_id]
    current_count = state["count"]

    new_count = (current_count + 1) % 5

    user_exercises_state[user_id]["count"] = new_count

    if new_count == 4:
        reply_markup = kb.forwardToLast_backward_d3
    elif new_count == 0:
        reply_markup = kb.forward_backwardToDays_d3
    else:
        reply_markup = kb.forward_backward_d3

    try:
        await callback.message.edit_media(media=exercises_d3[new_count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.delete()
        await callback.message.edit_media(media=exercises_d3[new_count], reply_markup=reply_markup)


@router.callback_query(F.data == 'backward_d3')
async def backward_d3(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 0, "level": "l3", "current_level": "l3"}

    state = user_exercises_state[user_id]
    current_count = state["count"]

    new_count = (current_count - 1) % 5

    user_exercises_state[user_id]["count"] = new_count

    if new_count > 0:
        reply_markup = kb.forward_backward_d3
    else:
        reply_markup = kb.forward_backwardToDays_d3

    try:
        await callback.message.edit_media(media=exercises_d3[new_count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.delete()
        await callback.message.edit_media(media=exercises_d3[new_count], reply_markup=reply_markup)


@router.callback_query(F.data == 'backward_to_days_d3')
async def backward_to_days_d3(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id in user_exercises_state:
        del user_exercises_state[user_id]

    await callback.message.delete()
    await callback.message.answer(
        'Выберите день тренировки (в неделе):',
        reply_markup=kb.days
    )


@router.callback_query(F.data == 'forward_to_last_d3')
async def forward_to_last_d3(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 4, "level": "l3", "current_level": "l3"}
    else:
        user_exercises_state[user_id]["count"] = 4

    await callback.message.delete()
    await callback.message.answer(text=ex.programForTraining_l3, reply_markup=kb.backwardToExercises_d3)


@router.callback_query(F.data == 'backward_to_exercises_d3')
async def backward_to_exercises_d3(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    if user_id not in user_exercises_state:
        user_exercises_state[user_id] = {"count": 4, "level": "l3", "current_level": "l3"}

    state = user_exercises_state[user_id]
    count = state["count"]

    if count == 4:
        reply_markup = kb.forwardToLast_backward_d3
    elif count == 0:
        reply_markup = kb.forward_backwardToDays_d3
    else:
        reply_markup = kb.forward_backward_d3

    try:
        await callback.message.edit_media(media=exercises_d3[count], reply_markup=reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        await callback.message.delete()
        await callback.message.edit_media(media=exercises_d3[count], reply_markup=reply_markup)


# Настройки --> вкл/выкл мотивацию + Подписка --> оплата
@router.message(Command('settings'))
async def settings(message: Message):
    await message.answer('⚙️ <b>НАСТРОЙКИ</b> ⚙️\n\nТут можно настроить своего бота.', reply_markup=kb.settings, parse_mode='HTML')

@router.callback_query(F.data == 'openSetting')
async def openSetting(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer('⚙️ <b>НАСТРОЙКИ</b> ⚙️\n\nТут можно настроить своего бота.', reply_markup=kb.settings, parse_mode='HTML')

@router.callback_query(F.data == 'backward_to_settings')
async def backward_to_settings(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('⚙️ <b>НАСТРОЙКИ</b> ⚙️\n\nТут можно настроить своего бота.', reply_markup=kb.settings)

@router.callback_query(F.data == 'motivation')
async def motivation_on(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('💯 <b>ЕЖЕДНЕВНАЯ МОТИВАЦИЯ</b> 💯\n\nТут можно включать\выключать мотивацию и выбирать время.',
                                     reply_markup=kb.motivation_setting, parse_mode='HTML')


@router.callback_query(F.data == 'motivation_on')
async def motivation_on(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.message.from_user.id
    subs = get_subscribers()
    if str(user_id) in subs and subs[str(user_id)]:
        return await callback.message.answer("🔔 Рассылка уже включена. Время: " + subs[str(user_id)])
    # Если пользователя нет — он должен выбрать время
    await callback.message.answer(
        "Чтобы включить рассылку, введите время в которое желаете получать сообщения:",
        reply_markup=kb.set_time
    )

@router.callback_query(lambda c: c.data == "motivation_off")
async def unsubscribe(callback: types.CallbackQuery):
    remove_user(callback.from_user.id)
    await callback.message.answer("🔕 Ты отписался от рассылки.")
    await callback.answer()


@router.callback_query(lambda c: c.data == "set_time")
async def ask_time(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("🕒 Введи время в формате <b>HH:MM</b> (например 14:30):")
    await state.set_state(UserTime.waiting_for_time)
    await callback.answer()

@router.callback_query(F.data == 'cancel_set_time')
async def cancel_set_time(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

# Принимаем пользовательское время
@router.message(UserTime.waiting_for_time)
async def save_time(message: types.Message, state: FSMContext):
    time_str = message.text.strip()
    import re
    if not re.fullmatch(r"[0-2]\d:[0-5]\d", time_str):
        await message.answer("❌ Неверный формат. Введи время как HH:MM, пример: 09:41")
        return
    set_user_time(message.from_user.id, time_str)
    await message.answer(
        f"Готово!\tТеперь сообщения будут приходить каждый день в <b>{time_str}</b> ⏰🔥"
    )
    await state.clear()



### Подписка
@router.callback_query(F.data == 'subscription')
async def subscription(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Информация о подписках:', reply_markup=kb.subscription_setting)

@router.callback_query(F.data == 'subscription_my')
async def subscription_my(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Информация о подписке пользователя')

@router.callback_query(F.data == 'subscription_pay')
async def subscription_my(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Оплата подписки')


# Профиль --> личные данные ...
@router.message(Command('profile'))
async def settings(message: Message):
    await message.answer('👤 <b>ПРОФИЛЬ</b> 👤\n\n Тут можно посмотреть свои личные данные.', reply_markup=kb.profile, parse_mode='HTML')

@router.callback_query(F.data == 'openProfile')
async def openSetting(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer('👤 <b>ПРОФИЛЬ</b> 👤\n\n Тут можно посмотреть свои личные данные.', reply_markup=kb.profile,
                                  parse_mode='HTML')

@router.callback_query(F.data == 'personal_info')
async def personal_info(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id

    try:
        user_data = await get_user_data(user_id)

        if not user_data:
            await callback.message.answer(
                "👤 <b>Профиль не найден</b>\n"
                "Зарегистрируйтесь и попробуйте снова (/reg).",
                parse_mode='HTML'
            )
            return

        name, height_cm, weight_kg = user_data

        message = (f'🔒 <b>ЛИЧНЫЕ ДАННЫЕ</b> 🔒\n\n'
                   f'<b>👤 Пользователь:</b> {name}\n'
                   f'<b>📏 Рост:</b> {height_cm} см ({height_cm / 100:.2f} м)\n'
                   f'<b>⚖️ Вес:</b> {weight_kg} кг')

        await callback.message.edit_text(message, reply_markup=kb.personal_info , parse_mode='HTML')

    except Exception as e:
        print(f"Ошибка при выводе личных данных пользователя {user_id}: {e}")
        await callback.message.answer(
            "⚠️ <b>Произошла ошибка</b>\n\n"
            "Пожалуйста, попробуйте позже или обратитесь к администратору (/help).",
            parse_mode='HTML'
        )

@router.callback_query(F.data == 'backward_to_profile')
async def backward_to_profile(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('👤 <b>ПРОФИЛЬ</b> 👤\n\n Тут можно посмотреть свои личные данные.', reply_markup=kb.profile,
                                  parse_mode='HTML')


async def delete_user_data(user_id: int) -> bool:
    try:
        async with aiosqlite.connect('coach_bot.db') as db:
            # Проверяем, существует ли пользователь перед удалением
            async with db.execute('SELECT 1 FROM athletes WHERE telegram_id = ? LIMIT 1', (user_id,)) as cursor:
                exists = await cursor.fetchone()

            if exists:
                await db.execute('DELETE FROM athletes WHERE telegram_id = ?', (user_id,))
                await db.commit()
                print(f"✅ Данные пользователя {user_id} удалены")
                return True
            else:
                print(f"ℹ️ Пользователь {user_id} не найден в БД")
                return False

    except Exception as e:
        print(f"❌ Database error while deleting user {user_id}: {e}")
        return False


@router.callback_query(F.data == 'edit_personal_info')
async def edit_personal_info_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id
    user_name = callback.from_user.full_name

    try:
        deletion_result = await delete_user_data(user_id)

        if deletion_result is None:
            await callback.answer("❌ Ошибка базы данных")
            await callback.message.answer("Произошла ошибка при работе с базой данных. Попробуйте позже.")
            return

        await asyncio.sleep(0.7)

        registration_msg = await callback.message.answer('Введите имя:')

        await state.update_data(
            registration_msg_id=registration_msg.message_id,
            user_id=user_id,
            username=user_name
        )

        await state.set_state(Reg.name_reg)

    except Exception as e:
        print(f"Error in edit_personal_info for user {user_id}: {e}")
        await callback.answer("❌ Произошла ошибка")
        await callback.message.answer("⚠️ Произошла непредвиденная ошибка. Попробуйте снова.")

@router.callback_query(F.data == 'delete_personal_info')
async def delete_personal_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('<b>Вы уверены что хотите удалить свой профиль?</b>\n\n'
                                  'Нажмите <i>\"Подтвердить\"</i> если да, и ваш профиль удалится.',
                                  reply_markup=kb.confirm_delete_personal_info, parse_mode='HTML')

@router.callback_query(F.data == 'confirm_delete_personal_info')
async def confirm_delete_personal_info(callback: CallbackQuery, state: FSMContext):

    await callback.answer()
    await delete_user_data(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer('✅ <b>Ваш профиль успешно удален!</b>\n\n'
                                  'Вы можете в любой момент зарегистрироваться заново по команде /reg',
                                  parse_mode='HTML')

@router.callback_query(F.data == 'cancel_delete_personal_info')
async def backward_to_personal_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()


### Индекс массы тела:
async def get_user_data(user_id: int) -> Optional[Tuple]:
    try:
        async with aiosqlite.connect('coach_bot.db') as db:
            cursor = await db.execute('SELECT name, height, weight FROM athletes WHERE telegram_id = ?', (user_id,))
            return await cursor.fetchone()
    except Exception as e:
        print(f"Database error: {e}")
        return None

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_bmi_category(bmi: float) -> dict:
    if bmi < 16:
        return {"name": "Выраженный дефицит", "emoji": "🏴‍☠️", "risk": "высокий"}
    elif 16 <= bmi < 18.5:
        return {"name": "Недостаточный вес", "emoji": "📉", "risk": "повышенный"}
    elif 18.5 <= bmi < 25:
        return {"name": "Нормальный вес", "emoji": "✅", "risk": "низкий"}
    elif 25 <= bmi < 30:
        return {"name": "Избыточный вес", "emoji": "⚠️", "risk": "повышенный"}
    elif 30 <= bmi < 35:
        return {"name": "Ожирение 1-й степени", "emoji": "🔴", "risk": "высокий"}
    elif 35 <= bmi < 40:
        return {"name": "Ожирение 2-й степени", "emoji": "🛑", "risk": "очень высокий"}
    else:
        return {"name": "Ожирение 3-й степени", "emoji": "🚨", "risk": "критический"}

@router.callback_query(F.data == 'body_mass_index')
async def body_mass_index(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id

    try:
        user_data = await get_user_data(user_id)

        if not user_data:
            await callback.message.answer(
                "👤 <b>Профиль не найден</b>\n\n"
                "Для расчета ИМТ необходимо создать профиль при помощи команды /reg.\n"
                "Зарегистрируйтесь и попробуйте снова.",
                parse_mode='HTML'
            )
            return

        name, height_cm, weight_kg = user_data

        bmi = calculate_bmi(weight_kg, height_cm)
        bmi_rounded = round(bmi, 1)

        category = get_bmi_category(bmi)

        message = f"""
{category['emoji']} <b>РАСЧЕТ ИНДЕКСА МАССЫ ТЕЛА</b> {category['emoji']}

<b>👤 Пользователь:</b> {name}
<b>📏 Рост:</b> {height_cm} см ({height_cm / 100:.2f} м)
<b>⚖️ Вес:</b> {weight_kg} кг

<b>🧮 Ваш ИМТ:</b> <code>{bmi_rounded}</code>

<b>📊 Категория:</b> {category['name']}
<b>⚠️ Уровень риска:</b> {category['risk']}

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Формула расчета: ИМТ = вес (кг) / [рост (м)]²
Ваш расчет: {weight_kg} / ({height_cm / 100:.2f})² = {bmi_rounded}</i>
"""
        file_path = FSInputFile('media/bmi.jpg')
        await callback.message.answer_photo(photo=file_path, caption=message, reply_markup=kb.backward_to_menu, parse_mode='HTML')

    except Exception as e:
        print(f"Ошибка при расчете ИМТ для пользователя {user_id}: {e}")
        await callback.message.answer(
            "⚠️ <b>Произошла ошибка</b>\n\n"
            "Пожалуйста, попробуйте позже или обратитесь к администратору (/help).",
            parse_mode='HTML'
        )

### Одноповторный максимум
@router.callback_query(F.data == 'one_rep_max')
async def one_rep_max(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Выберите упражнение у которого вы хотите вычислить свой разовый максимум:\n\n'
        '<i><b>Важно:</b> Точное значение одноповторного максимума зависит от многих индивидуальных особенностей организма '
        'каждого конкретного человека. Поэтому следует учитывать, что погрешность данных формул может составлять до 4%.\n'
        'А также чем большее количество повторений, тем менее точной становится формула. В идеале нужно выбрать вес, '
        'который можно поднять не более 10 раз.</i>',
                          reply_markup=kb.oneRepMax_choice, parse_mode='HTML')


# Жим лежа
@router.callback_query(F.data == 'bench_press_calculate')
async def bench_press_calculate_step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(exercise="жим лежа")
    await callback.message.answer('🏋️ <b>Жим лежа</b>\n\nВведите рабочий вес (в кг):', parse_mode='HTML')
    await state.set_state(OneRepMax.weight_1RM)

@router.message(OneRepMax.weight_1RM)
async def process1_weight(message: Message, state: FSMContext):
    weight_text = message.text.strip()

    try:
        weight = float(weight_text.replace(',', '.'))  # заменяем запятую на точку

        if weight <= 0:
            await message.answer('❌ Вес должен быть положительным числом! Попробуйте снова:')
            return

        if weight > 300:
            await message.answer('❌ Пожалуйста, введите реальный вес (не более 300 кг):')
            return
    except ValueError:
        await message.answer('❌ Неверный формат! Введите вес цифрами (например: 75 или 75.5):')
        return

    await state.update_data(weight=weight)

    await message.answer(f'✅ Вес <b>{weight} кг</b> сохранен.\n\nТеперь введите количество повторений:',
                         parse_mode='HTML')
    await state.set_state(OneRepMax.repetitions_1RM)

@router.message(OneRepMax.repetitions_1RM)
async def process1_repetitions(message: Message, state: FSMContext):
    repetitions_text = message.text.strip()

    try:
        # Пробуем преобразовать в целое число
        repetitions = int(repetitions_text)

        # Проверки
        if repetitions <= 0:
            await message.answer('❌ Количество повторений должно быть положительным числом! Попробуйте снова:')
            return

        if repetitions > 30:
            await message.answer('❌ Пожалуйста, введите реальное количество повторений (не более 30):')
            return

    except ValueError:
        await message.answer('❌ Неверный формат! Введите целое число повторений (например: 5 или 10):')
        return

    data = await state.get_data()
    weight = data.get('weight')
    exercise = data.get('exercise', 'упражнение')

    if not weight:
        await message.answer('❌ Ошибка: данные о весе не найдены. Начните заново.')
        await state.clear()
        return

    one_rep_max = weight * (1 + 0.025 * repetitions)
    one_rep_max_rounded = round(one_rep_max, 1)

    await message.answer(
        f'🏋️ <b>РЕЗУЛЬТАТ РАСЧЕТА 1RM</b>\n\n'
        f'<b>Упражнение:</b> {exercise}\n'
        f'<b>Рабочий вес:</b> {weight} кг\n'
        f'<b>Повторений:</b> {repetitions}\n'
        f'━━━━━━━━━━━━━━━━━━━━━━\n'
        f'<b>📍 Разовый максимум (1RM):</b>\t'
        f'<code>{one_rep_max_rounded} кг</code>\n\n'
        # f'<b>📊 Уровень сложности:</b> {difficulty}\n\n'
        f'<i>Рассчитано по формуле О\'Коннорa:\n'
        f'1 разовый максимум = M * (1 + 0.025 * k)\n'
        f'(M - вес штанги, k - количество повторений с этим весом)</i>',
        reply_markup=kb.backward_to_menu, parse_mode='HTML'
    )
    await state.clear()


# Приседания
@router.callback_query(F.data == 'squats_calculate')
async def squats_calculate_step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(exercise='приседания')
    await callback.message.answer('🏋️ <b>Приседания</b>\n\nВведите рабочий вес (в кг):', parse_mode='HTML')
    await state.set_state(OneRepMax.weight_1RM)

@router.message(OneRepMax.weight_1RM)
async def process2_weight(message: Message, state: FSMContext):
    weight_text = message.text.strip()

    try:
        weight = float(weight_text.replace(',', '.'))  # заменяем запятую на точку

        if weight <= 0:
            await message.answer('❌ Вес должен быть положительным числом! Попробуйте снова:')
            return

        if weight > 300:
            await message.answer('❌ Пожалуйста, введите реальный вес (не более 300 кг):')
            return
    except ValueError:
        await message.answer('❌ Неверный формат! Введите вес цифрами (например: 75 или 75.5):')
        return

    await state.update_data(weight=weight)

    await message.answer(f'✅ Вес <b>{weight} кг</b> сохранен.\n\nТеперь введите количество повторений:',
                         parse_mode='HTML')
    await state.set_state(OneRepMax.repetitions_1RM)

@router.message(OneRepMax.repetitions_1RM)
async def process2_repetitions(message: Message, state: FSMContext):
    repetitions_text = message.text.strip()

    try:
        # Пробуем преобразовать в целое число
        repetitions = int(repetitions_text)

        # Проверки
        if repetitions <= 0:
            await message.answer('❌ Количество повторений должно быть положительным числом! Попробуйте снова:')
            return

        if repetitions > 30:
            await message.answer('❌ Пожалуйста, введите реальное количество повторений (не более 30):')
            return

    except ValueError:
        await message.answer('❌ Неверный формат! Введите целое число повторений (например: 5 или 10):')
        return

    data = await state.get_data()
    weight = data.get('weight')
    exercise = data.get('exercise', 'упражнение')

    if not weight:
        await message.answer('❌ Ошибка: данные о весе не найдены. Начните заново.')
        await state.clear()
        return

    one_rep_max = weight * (1 + 0.025 * repetitions)
    one_rep_max_rounded = round(one_rep_max, 1)

    await message.answer(
        f'🏋️ <b>РЕЗУЛЬТАТ РАСЧЕТА 1RM</b>\n\n'
        f'<b>Упражнение:</b> {exercise}\n'
        f'<b>Рабочий вес:</b> {weight} кг\n'
        f'<b>Повторений:</b> {repetitions}\n'
        f'━━━━━━━━━━━━━━━━━━━━━━\n'
        f'<b>📍 Разовый максимум (1RM):</b>\t'
        f'<code>{one_rep_max_rounded} кг</code>\n\n'
        # f'<b>📊 Уровень сложности:</b> {difficulty}\n\n'
        f'<i>Рассчитано по формуле О\'Коннорa:\n'
        f'1 разовый максимум = M * (1 + 0.025 * k)\n'
        f'(M - вес штанги, k - количество повторений с этим весом)</i>',
        reply_markup=kb.backward_to_menu, parse_mode='HTML'
    )
    await state.clear()


# Становая тяга
@router.callback_query(F.data == 'deadlift_calculate')
async def squats_calculate_step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(exercise='становая тяга')
    await callback.message.answer('🏋️ <b>Приседания</b>\n\nВведите рабочий вес (в кг):', parse_mode='HTML')
    await state.set_state(OneRepMax.weight_1RM)

router.message(OneRepMax.weight_1RM)
async def process3_weight(message: Message, state: FSMContext):
    weight_text = message.text.strip()

    try:
        weight = float(weight_text.replace(',', '.'))  # заменяем запятую на точку

        if weight <= 0:
            await message.answer('❌ Вес должен быть положительным числом! Попробуйте снова:')
            return

        if weight > 300:
            await message.answer('❌ Пожалуйста, введите реальный вес (не более 300 кг):')
            return
    except ValueError:
        await message.answer('❌ Неверный формат! Введите вес цифрами (например: 75 или 75.5):')
        return

    await state.update_data(weight=weight)

    await message.answer(f'✅ Вес <b>{weight} кг</b> сохранен.\n\nТеперь введите количество повторений:',
                         parse_mode='HTML')
    await state.set_state(OneRepMax.repetitions_1RM)

@router.message(OneRepMax.repetitions_1RM)
async def process3_repetitions(message: Message, state: FSMContext):
    repetitions_text = message.text.strip()

    try:
        # Пробуем преобразовать в целое число
        repetitions = int(repetitions_text)

        # Проверки
        if repetitions <= 0:
            await message.answer('❌ Количество повторений должно быть положительным числом! Попробуйте снова:')
            return

        if repetitions > 30:
            await message.answer('❌ Пожалуйста, введите реальное количество повторений (не более 30):')
            return

    except ValueError:
        await message.answer('❌ Неверный формат! Введите целое число повторений (например: 5 или 10):')
        return

    data = await state.get_data()
    weight = data.get('weight')
    exercise = data.get('exercise', 'упражнение')

    if not weight:
        await message.answer('❌ Ошибка: данные о весе не найдены. Начните заново.')
        await state.clear()
        return

    one_rep_max = weight * (1 + 0.025 * repetitions)
    one_rep_max_rounded = round(one_rep_max, 1)

    await message.answer(
        f'🏋️ <b>РЕЗУЛЬТАТ РАСЧЕТА 1RM</b>\n\n'
        f'<b>Упражнение:</b> {exercise}\n'
        f'<b>Рабочий вес:</b> {weight} кг\n'
        f'<b>Повторений:</b> {repetitions}\n'
        f'━━━━━━━━━━━━━━━━━━━━━━\n'
        f'<b>📍 Разовый максимум (1RM):</b>\t'
        f'<code>{one_rep_max_rounded} кг</code>\n\n'
        # f'<b>📊 Уровень сложности:</b> {difficulty}\n\n'
        f'<i>Рассчитано по формуле О\'Коннорa:\n'
        f'1 разовый максимум = M * (1 + 0.025 * k)\n'
        f'(M - вес штанги, k - количество повторений с этим весом)</i>',
        reply_markup=kb.backward_to_menu, parse_mode='HTML'
    )
    await state.clear()


### Партнеры
@router.callback_query(F.data == 'view_partners')
async def view_partners(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('<b>Здесь представлены наши партнеры.</b>', reply_markup=kb.partners, parse_mode='HTML')

@router.callback_query(F.data == 'backward_to_partners')
async def backward_to_partners(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Тут представлены наши партнеры', reply_markup=kb.partners, parse_mode='HTML')

@router.callback_query(F.data == 'view_partner1')
async def view_partner1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f'<b>{partner}</b>\n\n'
                                     'Устал от бесконечного скролла в общих чатах, где невозможно никого нормально узнать? Мы тоже.\n\n'
                                     'Поэтому мы, такие же первокурсники-разработчики, сделали <b>KNRTU DATING APP</b> '
                                     '— уютную площадку для знакомств в рамках нашего университета. Здесь можно:\n\n'
                                     '• Найти соседа в общагу или партнёра по спортзалу 💪\n\n'
                                     '• Обсудить сложную лабу с тем, кто её уже сдал 🧠\n\n'
                                     '• Создать или найти компанию для тусовки 🎉\n\n'
                                     '• И да, конечно, познакомиться с кем-то особенным ❤️\n\n'
                                     'Без лишней сложности. Без фейков. Только свой университетский круг. '
                                     'Регистрируйся и начни общаться по-настоящему!\n\n'
                                     '<b>Сайт:</b> https://dating-site-mu.vercel.app/',
                                     reply_markup=kb.partner1, parse_mode='HTML')


# Регистрация --> имя --> рост --> вес --> сохранение в бд
async def user_exists(telegram_id: int) -> bool:
    try:
        async with aiosqlite.connect('coach_bot.db') as db:
            async with db.execute(
                "SELECT 1 FROM athletes WHERE telegram_id = ? LIMIT 1",
                (telegram_id,)
            ) as cursor:
                result = await cursor.fetchone()
                return result is not None
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False

@router.message(Command('reg'))
async def reg_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if await user_exists(telegram_id):
        await message.answer("✅ Вы уже зарегистрированы в системе!")
        return
    await message.answer('Введите ваше имя:')
    await state.set_state(Reg.name_reg)

@router.message(Reg.name_reg)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await message.answer('Введите ваш рост (в см):')
    await state.set_state(Reg.height_reg)

@router.message(Reg.height_reg)
async def get_name(message: Message, state: FSMContext):
    height_text = message.text.strip()
    # ПРОВЕРКА: является ли ввод числом
    try:
        # Пробуем преобразовать в число (целое или дробное)
        weight = float(height_text)
        # Дополнительная проверка: вес должен быть положительным
        if weight <= 0:
            await message.answer('Рост должен быть положительным числом! Попробуйте снова:')
            return  # Остаёмся в том же состоянии
        # Можно также проверить на реалистичность веса
        if weight > 300:
            await message.answer('Пожалуйста, введите реальный рост (не более 230 см):')
            return
    except ValueError:
        await message.answer('❌ Неверный формат! Введите рост цифрами (например: 180 или 180.5):')
        return
    await state.update_data(height=height_text)
    await message.answer('Введите ваш вес (в кг):')
    await state.set_state(Reg.weight_reg)

@router.message(Reg.weight_reg)
async def get_weight(message: Message, state: FSMContext):
    weight_text  = message.text.strip()
    try:
        weight = float(weight_text)
        if weight <= 0:
            await message.answer('Вес должен быть положительным числом! Попробуйте снова:')
            return
        if weight > 300:
            await message.answer('Пожалуйста, введите реальный вес (не более 300 кг):')
            return
    except ValueError:
        await message.answer('❌ Неверный формат! Введите вес цифрами (например: 75 или 75.5):')
        return
    data = await state.get_data()
    name = data['name']
    height = data['height']
    telegram_id = message.from_user.id
    await add_athletes_to_database(telegram_id, name, height, weight)
    await message.answer(f'✅ <b>Отлично, вы зарегистрированы!</b>\n\n'
                         f'👤 <b>Имя:</b> {name}\n'
                         f'📏 <b>Рост:</b> {height} см\n'
                         f'⚖️ <b>Вес:</b> {weight} кг',
                         reply_markup=kb.backward_to_menu, parse_mode='HTML')
    print('athlete registered')
    await state.clear()


