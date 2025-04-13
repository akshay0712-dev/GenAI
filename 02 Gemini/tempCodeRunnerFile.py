from dotenv import load_dotenv
import os
import json
from google import genai
from google.genai import types

load_dotenv() 
api_key = os.getenv("API_KEY")
# Only run this block for Gemini Developer API
client = genai.Client(api_key = api_key)