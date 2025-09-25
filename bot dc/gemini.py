import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # You can inspect the error message here if needed
        error_message = str(e)
        if "rate limit" in error_message.lower():
            return "⚠️ You've reached the free API usage limit. Please try again later."
        return f"❌ An error occurred: {error_message}"