
import os
from dotenv import load_dotenv
from google import genai

# Step 1: Load environment variables
load_dotenv()

# Step 2: Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Step 3: Check API key
if not api_key:
    raise ValueError("Gemini API key not found!")

# Step 4: Create Gemini client
client = genai.Client(api_key=api_key)

# Step 5: Send a prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Introduce yourself as an AI technical interviewer in 3 sentences."
)

# Step 6: Display AI response
print("\nGemini AI Response:")
print(response.text)
