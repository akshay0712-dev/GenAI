from dotenv import load_dotenv
import os
import json
from google import genai
from google.genai import types

load_dotenv() 
api_key = os.getenv("API_KEY")
# Only run this block for Gemini Developer API
client = genai.Client(api_key = api_key)


system_prompt = """

"""
while True:
    messages = []

    user_input = input("Enter your query: ")
    messages.append(user_input)

    while True: 
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
            contents=messages,
        )
        # print("response text: ", response.text)
        clean_text = response.text.strip()

        if clean_text.startswith("```json"):
            clean_text = clean_text.removeprefix("```json").removesuffix("```").strip()

        elif clean_text.startswith("{{") and clean_text.endswith("}}"):
            clean_text = clean_text[1:-1].strip()  
        # print("clean text: ", clean_text)
        parsed_response = json.loads(clean_text)
        messages.append(clean_text)
        

        if parsed_response.get("step") != "result" :
            print(f"🧠 {parsed_response.get("step")}: {parsed_response.get("content")} " )
            continue

        print(f"🤖  {parsed_response.get("step")}: {parsed_response.get("content")}")
        break
# print(messages)