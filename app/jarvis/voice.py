import edge_tts
import asyncio
import tempfile
import os
import requests
from app.core.config import settings

VOICE = "en-GB-RyanNeural"

GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

async def _generate_speech(text: str, output_file: str):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def speak(text: str):
    """Text to Speech"""
    try:
        import pygame

        text = str(text).replace("**", "").replace("*", "").replace("#", "").strip()
        if len(text) < 2:
            return

        if len(text) > 600:
            text = text[:600] + "..."

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        asyncio.run(_generate_speech(text, temp_path))

        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()
        pygame.mixer.quit()

        try:
            os.unlink(temp_path)
        except:
            pass

    except Exception as e:
        print(f"TTS Error: {e}")

def speech_to_text(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """Convert speech audio to text using Groq Whisper"""
    try:
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}"
        }

        files = {
            "file": (filename, audio_bytes, "audio/wav"),
        }

        data = {
            "model": "whisper-large-v3",
            "language": "en",  # can change later
            "response_format": "text"
        }

        response = requests.post(
            GROQ_STT_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )

        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Speech recognition error: {str(e)}"