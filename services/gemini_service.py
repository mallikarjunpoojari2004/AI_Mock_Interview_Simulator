
import os
import time
from dotenv import load_dotenv
from google import genai

# Step 1: Load environment variables
load_dotenv()

# Step 2: Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Step 3: Validate API key
if not api_key:
    raise ValueError("Gemini API key not found!")

# Step 4: Create Gemini client
client = genai.Client(api_key=api_key)

# Step 5: Select Gemini model
MODEL_NAME = "gemini-3.5-flash-lite"


# Step 6: Generate AI response
def generate_response(prompt):

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                print(f"Gemini busy. Retry {attempt + 1}/3")

                if attempt < 2:
                    time.sleep(5)
                else:
                    return "Gemini is temporarily unavailable. Try again later."

            else:
                return f"Gemini API Error: {error_message}"
