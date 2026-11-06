
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Check whether API key exists
if api_key:
    print("Gemini API key loaded successfully!")
else:
    print("Gemini API key not found!")
