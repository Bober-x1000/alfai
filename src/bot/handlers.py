from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .bot import TrainingStates
from .keyboards import start_keyboard, case_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для тренировки бизнес-мышлений.\n"
        "Нажми кнопку ниже, чтобы начать тренинг.",
        reply_markup=start_keyboard()
    )

@router.callback_query(lambda c: c.data == "start_training")
async def process_start_training(callback: CallbackQuery, state: FSMContext):
    # Импорт giga_client внутри функции
    from .bot import giga_client

    if not giga_client:
        await callback.message.answer("GigaChat не инициализирован. Обратитесь к администратору.")
        await callback.answer()
        return

    # Генерируем 5 кейсов
    cases = {}
    for i in range(1, 6):
        case = await giga_client.generate_case(i)
        cases[f"case_{i}"] = case

    await state.update_data(cases=cases)
    await callback.message.edit_text(
        "Выбери бизнес-кейс для решения:",
        reply_markup=case_keyboard()
    )
    await state.set_state(TrainingStates.waiting_for_case_selection)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("case_"))
async def process_case_selection(callback: CallbackQuery, state: FSMContext):
    from .bot import giga_client

    if not giga_client:
        await callback.message.answer("GigaChat не инициализирован. Обратитесь к администратору.")
        await callback.answer()
        return

    case_id = callback.data
    data = await state.get_data()
    cases = data.get("cases", {})
    case_text = cases.get(case_id, "Кейс не найден")
    
    await callback.message.edit_text(
        f"🎯 Кейс:\n{case_text}\n\n"
        "Напиши свое решение и я его оценю:"
    )
    # ✅ await перед update_data
    await state.update_data(selected_case_id=case_id, selected_case_text=case_text)
    await state.set_state(TrainingStates.waiting_for_solution)
    await callback.answer()

@router.message(TrainingStates.waiting_for_solution)
async def process_user_solution(message: Message, state: FSMContext):
    from .bot import giga_client

    if not giga_client:
        await message.answer("GigaChat не инициализирован. Обратитесь к администратору.")
        await state.clear()
        return

    user_solution = message.text
    data = await state.get_data()
    case_text = data.get("selected_case_text")
    
    if not case_text:
        await message.answer("Ошибка: кейс не выбран. Начни заново с /start")
        await state.clear()
        return

    # Оценка решения через GigaChat
    evaluation = await giga_client.evaluate_solution(case_text, user_solution)
    
    await message.answer(
        f"Твое решение:\n{user_solution}\n\n"
        f"Оценка и анализ:\n{evaluation}\n\n"
        f"Хочешь решить ещё кейс? Нажми /start"
    )
    
    await state.clear()