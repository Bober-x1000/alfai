import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup  # ← Правильный импорт
from aiogram.fsm.storage.memory import MemoryStorage  # ← Добавить

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)  # ← Создаем с storage

# Состояния пользователя
class TrainingStates(StatesGroup):
    waiting_for_case_selection = State()
    waiting_for_solution = State()

giga_client = None

def setup_services(giga: "GigaChatClient"):
    global giga_client
    giga_client = giga