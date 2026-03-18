import os
from groq import Groq
from gtts import gTTS

class AudioProcessor:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY is not set.")
        self.groq_client = Groq(api_key=api_key)

    def stt(self, audio_file_path: str) -> str:
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.groq_client.audio.transcriptions.create(
                  file=(audio_file_path, file.read()),
                  model="whisper-large-v3",
                  language="uk"
                )
            return transcription.text
        except Exception as e:
            print(f"STT Error: {e}")
            return ""

    def tts(self, text: str, output_path: str):
        try:
            tts = gTTS(text=text, lang="uk")
            tts.save(output_path)
            return True
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
