import asyncio
import os
from dotenv import load_dotenv

# Импорты из пакетов
from src.bot.bot import bot, dp, setup_services
from src.api.gigachat_client import GigaChatClient

# Импорты обработчиков после инициализации
from src.bot.handlers import router

load_dotenv()

async def main():
    # Инициализация клиента
    giga_client = GigaChatClient()
    await giga_client.initialize()

    # Передача клиента в bot.py
    setup_services(giga_client)

    # Теперь можно подключать роутер (после setup_services)
    dp.include_router(router)

    print("🚀 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())