import os
from dotenv import load_dotenv

load_dotenv()
try:
    from core.llm_engine import CulinaryAssistant
    from core.audio_processor import AudioProcessor

    print("Init LLM...")
    assistant = CulinaryAssistant()
    print("Testing LLM...")
    response = assistant.get_response("Привіт, я маю картоплю та курку. Що приготувати?")
    print("LLM Response:\n", response)

    print("Init Audio...")
    audio = AudioProcessor()
    
    print("Testing TTS...")
    audio.tts(response, "test_audio.mp3")
    print("TTS File Created:", os.path.exists("test_audio.mp3"))
    
    if os.path.exists("test_audio.mp3"):
        os.remove("test_audio.mp3")
        
    print("Test passed successfully.")
except Exception as e:
    print(f"Test failed: {e}")
