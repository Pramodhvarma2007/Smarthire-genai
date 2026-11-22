import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")

if not API_KEY:
    raise ValueError("LLM_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello to SmartHire-GenAI!"
)

print(response.text)