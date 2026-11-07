
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


def transcribe_audio(audio_bytes, question=None):

    try:

        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/wav"
        )

        prompt = f"""
        You are a professional technical interview speech transcriber.

        Interview Question:
        {question if question else "General interview question"}

        Transcribe the candidate's spoken answer accurately.

        IMPORTANT INSTRUCTIONS:

        1. Preserve the candidate's actual spoken words.
        2. Recognize programming terminology correctly.
        3. Pay special attention to Java, Python, SQL and programming concepts.
        4. Recognize spoken keywords such as:
           public, static, void, int, String, class, return,
           if, else, for, while, try, catch and throw.
        5. Recognize programming terms such as:
           array, index, variable, method, function,
           object, loop and condition.
        6. If the candidate speaks code syntax, preserve
           the spoken sequence as accurately as possible.
        7. Recognize spoken symbols when clearly dictated:
           parentheses, curly braces, square brackets,
           semicolon, equals, greater than and less than.
        8. Do not invent missing code or programming statements.
        9. Do not silently correct the candidate's mistakes.
        10. Do not evaluate or improve the answer.

        Return only the transcribed answer.
        """

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                prompt,
                audio_part
            ]
        )

        return response.text

    except Exception as e:

        return f"Transcription Error: {str(e)}"
