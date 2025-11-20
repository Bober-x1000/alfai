from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    """Клавиатура для команды /start"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать тренинг", callback_data="start_training")]
    ])
    return keyboard

def case_keyboard():
    """Клавиатура для выбора бизнес-кейса"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кейс 1", callback_data="case_1")],
        [InlineKeyboardButton(text="Кейс 2", callback_data="case_2")],
        [InlineKeyboardButton(text="Кейс 3", callback_data="case_3")],
        [InlineKeyboardButton(text="Кейс 4", callback_data="case_4")],
        [InlineKeyboardButton(text="Кейс 5", callback_data="case_5")]
    ])
    return keyboard