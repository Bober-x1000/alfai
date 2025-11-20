import os
from gigachat import GigaChat
import asyncio

class GigaChatClient:
    def __init__(self, credentials: str = None):
        self.credentials = credentials or os.getenv("GIGACHAT_CREDENTIALS")
        self.verify_ssl_certs = os.getenv("GIGACHAT_VERIFY_SSL", "False").lower() == "true"
        self.client = None

    async def initialize(self):
        if not self.credentials:
            raise ValueError("GigaChat credentials not provided")
        self.client = GigaChat(credentials=self.credentials, verify_ssl_certs=self.verify_ssl_certs)

    async def generate_case(self, case_number: int) -> str:
        """Генерация бизнес-кейса"""
        prompt = f"""
        Сгенерируй бизнес-кейс под номером {case_number}. 
        Опиши реальную деловую ситуацию, с которой может столкнуться компания.
        Не пиши "Кейс {case_number}:", просто опиши ситуацию.
        """
        try:
            # ✅ Правильный вызов: передаем строку напрямую
            response = await self.client.achat(prompt)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Ошибка при генерации кейса: {str(e)}"

    async def evaluate_solution(self, case: str, user_solution: str) -> str:
        """Оценка решения пользователя"""
        prompt = f"""
        Кейс: {case}
        
        Решение пользователя: {user_solution}
        
        Оцени решение по 10-балльной шкале и дай конструктивный фидбэк.
        Укажи, что хорошо, что можно улучшить, и предложи альтернативные идеи.
        """
        try:
            response = await self.client.achat(prompt)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Ошибка при оценке решения: {str(e)}"

    async def generate_example_solution(self, case: str) -> str:
        """Генерация эталонного решения"""
        prompt = f"""
        Кейс: {case}
        
        Предложи эталонное решение для этого кейса. 
        Сформулируй его как пример хорошего бизнес-мышления.
        """
        try:
            response = await self.client.achat(prompt)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Ошибка при генерации эталонного решения: {str(e)}"