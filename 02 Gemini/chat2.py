from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv() 
api_key = os.getenv("API_KEY")
# Only run this block for Gemini Developer API
client = genai.Client(api_key='AIzaSyAKPsVOicq0wsLJjEVrtVQNg_eEu_5z_8Q')

system_prompt = """
You are an AI Assistant who is specialized in maths.
You should not answer any query that is not related to maths.

For a given query help user to solve that along with explanation.

Example:
Input: 2 + 2
Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

Input: 3 * 10
Output: 3 * 10 is 30 which is calculated by multipling 3 by 10. Funfact you can even multiply 10 * 3 which gives same result.

Input: Why is sky blue?
Output: Bruh? You alright? Is it maths query?
"""

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='What is life?',
    config=types.GenerateContentConfig(
        # system_instruction= system_prompt,
        max_output_tokens=1000,
        temperature=0.1,

    ),
)
print(response.text)