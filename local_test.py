import os
import sys
from dotenv import load_dotenv

load_dotenv()

from core.llm_engine import CulinaryAssistant
from core.audio_processor import AudioProcessor

def main():
    print("=== Локальне тестування Кулінарного Помічника ===")
    print("Ініціалізація...")
    
    assistant = CulinaryAssistant()
    audio = AudioProcessor()
    
    print("\nБот готовий. Введіть текст для спілкування. Для виходу введіть 'exit'.")
    print("Текст також буде озвучено і збережено у файлі 'response.mp3' (симуляція TTS).")
    
    while True:
        try:
            user_input = input("\nВи: ")
            if user_input.lower() in ('exit', 'quit', 'вихід'):
                print("Завершення роботи.")
                break
                
            print("Бот думає...")
            response_text = assistant.get_response(user_input)
            print(f"Бот: {response_text}")
            
            print("Синтез мовлення...")
            success = audio.tts(response_text, "response.mp3")
            if success:
                print("-> Збережено response.mp3")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
