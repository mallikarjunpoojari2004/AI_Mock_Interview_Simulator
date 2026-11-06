
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


def transcribe_audio(audio_bytes):
    """
    Convert recorded interview audio into text.
    """

    try:
        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/wav"
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                "Transcribe the spoken words exactly. Return only the transcript.",
                audio_part
            ]
        )

        return response.text

    except Exception as e:
        return f"Transcription Error: {str(e)}"
