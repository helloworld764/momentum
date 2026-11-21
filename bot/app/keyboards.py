from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать тренировку!', callback_data='startTraning')],
    [InlineKeyboardButton(text='Настройки', callback_data='openSetting'), InlineKeyboardButton(text='Профиль', callback_data='openProfile')],
    [InlineKeyboardButton(text='Наши партнеры', callback_data='view_partners'), InlineKeyboardButton(text='Наш сайт',
                                                                        url='https://helloworld764.github.io/momentum_bot_by_knitu/#anatomy')]
])


backward_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню', callback_data='backward_to_menu')]
])


### ТРЕНИРОВКА
continue_backward_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продолжить', callback_data='continue_to_days')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_menu')]
])

days = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='День 1', callback_data='first_day')],
    [InlineKeyboardButton(text='День 2', callback_data='second_day')],
    [InlineKeyboardButton(text='День 3', callback_data='third_day')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_continue')]
])

### НАЧАЛЬНЫЙ УРОВЕНЬ
forward_backward_d1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d1'), InlineKeyboardButton(text='Вперед', callback_data='forward_d1')],
])

forward_backwardToDays_d1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_days_d1'), InlineKeyboardButton(text='Вперед', callback_data='forward_d1')],
])

forwardToLast_backward_d1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d1'), InlineKeyboardButton(text='Вперед', callback_data='forward_to_last_d1')],
])

backward_d1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d1')]
])

backwardToExercises_d1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_exercises_d1')],
    [InlineKeyboardButton(text='Главное меню', callback_data='backward_to_menu')]
])

### СРЕДНИЙ УРОВЕНЬ
forward_backward_d2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d2'), InlineKeyboardButton(text='Вперед', callback_data='forward_d2')],
])

forward_backwardToDays_d2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_days_d2'), InlineKeyboardButton(text='Вперед', callback_data='forward_d2')],
])

forwardToLast_backward_d2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d2'), InlineKeyboardButton(text='Вперед', callback_data='forward_to_last_d2')],
])

backward_d2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d2')]
])

backwardToExercises_d2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_exercises_d2')],
    [InlineKeyboardButton(text='Главное меню', callback_data='backward_to_menu')]
])

### ПРОДВИНУТЫЙ УРОВЕНЬ
forward_backward_d3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d3'), InlineKeyboardButton(text='Вперед', callback_data='forward_d3')],
])

forward_backwardToDays_d3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_days_d3'), InlineKeyboardButton(text='Вперед', callback_data='forward_d3')],
])

forwardToLast_backward_d3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d3'), InlineKeyboardButton(text='Вперед', callback_data='forward_to_last_d3')],
])

backward_d3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_d3')]
])

backwardToExercises_d3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_exercises_d3')],
    [InlineKeyboardButton(text='Главное меню', callback_data='backward_to_menu')]
])


### НАСТРОЙКИ
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ежедневая мотивация', callback_data='motivation')],
    [InlineKeyboardButton(text='Подписка', callback_data='subscription')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_menu')]
])

# backward_to_settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Назад', callback_data='backward_to_settings')],
# ])

motivation_setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вкл. мотивацию', callback_data='motivation_on'), InlineKeyboardButton(text='Выкл. мотивацию', callback_data='motivation_off')],
    [InlineKeyboardButton(text='Изменить время', callback_data='set_time')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_settings')]
])
set_time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Установить время', callback_data='set_time')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_set_time')]
])

subscription_setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Моя подписка', callback_data='subscription_my'), InlineKeyboardButton(text='Оплатить', callback_data='subscription_pay')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_settings')]
])



### ПРОФИЛЬ
profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Личные данные', callback_data='personal_info')],
    # [InlineKeyboardButton(text='Статистика', callback_data='statistics')],
    [InlineKeyboardButton(text='Рассчитать индекс массы тела (ИМТ)', callback_data='body_mass_index')],
    [InlineKeyboardButton(text='Рассчитать разовый максимум (1ПМ)', callback_data='one_rep_max')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_menu')]
])

personal_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить данные', callback_data='edit_personal_info')],
    [InlineKeyboardButton(text='Удалить профиль', callback_data='delete_personal_info')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_profile')]
])

confirm_delete_personal_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='confirm_delete_personal_info')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_delete_personal_info')]
])

oneRepMax_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Жим лёжа', callback_data='bench_press_calculate')],
    [InlineKeyboardButton(text='Приседания', callback_data='squats_calculate')],
    [InlineKeyboardButton(text='Становая тяга', callback_data='deadlift_calculate')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_profile')]
])


### Партнеры
partners = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='KNRTU DATING APP', callback_data='view_partner1')],
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_menu')],
])

partner1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='backward_to_partners')],
    [InlineKeyboardButton(text='Главное меню', callback_data='backward_to_menu')]
])
