from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv() 
api_key = os.getenv("API_KEY")
# Only run this block for Gemini Developer API
client = genai.Client(api_key = api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.1,
    ),
    contents='What is the square root of 1441?',
)
print(response.text)