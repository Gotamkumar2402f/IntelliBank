import os
from dotenv import load_dotenv
load_dotenv()
import edge_tts
import asyncio
import tempfile
import requests

VOICE = "en-GB-RyanNeural"
GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"


async def _generate_speech(text: str, output_file: str):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)


def speak(text: str, lang: str = "en"):
    """Text to Speech — supports English + Urdu voice."""
    try:
        import pygame

        text = str(text).replace("**", "").replace("*", "").replace("#", "").strip()
        if len(text) < 2:
            return

        if len(text) > 600:
            text = text[:600] + "..."

        if lang == "ur":
            voice = "ur-PK-AsadNeural"
        elif lang == "hi":
            voice = "hi-IN-MadhurNeural"
        else:
            voice = VOICE

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        async def _gen():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(temp_path)

        asyncio.run(_gen())

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


def detect_language(text: str) -> str:
    """Detect if text is Urdu, Roman Urdu, Hindi, or English."""
    if not text:
        return "en"

    # Urdu script
    urdu_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    if urdu_chars > 3:
        return "ur"

    # Hindi script
    hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    if hindi_chars > 3:
        return "hi"

    # Roman Urdu keywords
    roman_urdu_words = [
        "kya", "kaise", "kitna", "kitni", "kitne", "hai", "hain", "ka",
        "ki", "ke", "me", "mein", "dikhao", "batao", "bata", "karo",
        "chahiye", "mujhe", "mera", "meri", "aap", "tum", "bhai",
        "acha", "theek", "nahi", "haan", "kab", "kahan", "kaun"
    ]
    text_lower = text.lower()
    roman_matches = sum(1 for w in roman_urdu_words if w in text_lower)
    if roman_matches >= 2:
        return "roman_ur"

    return "en"


def speech_to_text(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """Convert speech to text using Groq Whisper — English forced with banking context."""
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
        }

        files = {
            "file": (filename, audio_bytes, "audio/wav"),
        }

        data = {
            "model": "whisper-large-v3",
            "response_format": "text",
            "temperature": "0.0",
            "language": "en",  # 🇬🇧 Force English (avoids Chinese/Indonesian misfires)
            "prompt": "Banking assistant. Transactions, fraud, PDF summary, account balance, Jarvis."
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