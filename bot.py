import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Voice, FSInputFile
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from core.audio_processor import AudioProcessor
from core.llm_engine import CulinaryAssistant

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    print("КРИТИЧНА ПОМИЛКА: Не знайдено TG_BOT_TOKEN у файлі .env.")
    print("Будь ласка, додайте токен вашого бота і перезапустіть.")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
audio_processor = AudioProcessor()

user_sessions = {}

def get_assistant(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = CulinaryAssistant()
    return user_sessions[user_id]


@dp.message(CommandStart())
async def cmd_start(message: Message):
    assistant = get_assistant(message.from_user.id)
    welcome_text = assistant.get_response("Привіт! Я новий користувач. Що ти вмієш?")
    await message.answer(welcome_text)


@dp.message(F.text)
async def handle_text(message: Message):
    assistant = get_assistant(message.from_user.id)
    response_text = assistant.get_response(message.text)
    await message.answer(response_text)


@dp.message(F.voice)
async def handle_voice(message: Message):
    user_id = message.from_user.id
    assistant = get_assistant(user_id)
    
    processing_msg = await message.answer("Слухаю та обробляю...")
    
    file = await bot.get_file(message.voice.file_id)
    input_audio_path = f"user_{user_id}_voice.ogg"
    await bot.download_file(file.file_path, destination=input_audio_path)
    
    text_from_voice = audio_processor.stt(input_audio_path)
    
    if not text_from_voice.strip():
        await processing_msg.edit_text("Не вдалося розпізнати текст. Спробуйте говорити чіткіше.")
        return
        
    await processing_msg.edit_text(f"Ви сказали: <i>{text_from_voice}</i>", parse_mode="HTML")
    
    response_text = assistant.get_response(text_from_voice)
    
    output_audio_path = f"bot_{user_id}_response.mp3"
    success = audio_processor.tts(response_text, output_audio_path)
    
    if success:
        try:
            voice_response = FSInputFile(output_audio_path)
            await message.answer_voice(voice=voice_response, caption=response_text)
        except Exception as e:
            logging.error(f"Помилка відправки голосового: {e}")
            await message.answer(response_text)
    else:
        await message.answer(response_text)
        
    if os.path.exists(input_audio_path):
        os.remove(input_audio_path)
    if os.path.exists(output_audio_path):
        os.remove(output_audio_path)


async def main():
    print("Бот запущений і готовий приймати повідомлення!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
