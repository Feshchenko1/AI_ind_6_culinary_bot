import os
from google import genai

class CulinaryAssistant:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY is not set.")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"
        
        self.system_instruction = (
            "Ти — інтерактивний кулінарний помічник (Варіант 14). "
            "Твоя мета: "
            "1. Запитувати, які інгредієнти є у користувача. "
            "2. Пропонувати рецепти на основі наявних інгредієнтів. "
            "3. Інструктувати користувача під час приготування покроково. Не видавай всі кроки одразу. Чекай, поки користувач скаже, що він готовий до наступного кроку. "
            "4. Відстежувати динамічне оновлення інгредієнтів. Якщо користувач каже 'я замість вершкового масла використовую кокосову олію', май це на увазі в подальших кроках і підтверди заміну. "
            "Відповідай коротко (зазвичай 1-3 речення), лаконічно і привітно. Готуй текст для голосового синтезу (уникай складного мардауну, смайликів та спецсимволів, коли це можливо)."
        )
        
        self.chat = self.client.chats.create(
            model=self.model_id,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.7,
            )
        )

    def get_response(self, user_text: str) -> str:
        try:
            response = self.chat.send_message(user_text)
            return response.text
        except Exception as e:
            print(f"LLM Error: {e}")
            return "Вибачте, сталася помилка при обробці вашого запиту."
