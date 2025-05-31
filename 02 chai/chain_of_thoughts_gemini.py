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
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
{{ "step": "string", conte"nt: "string" }}

Example:
Input: What is 2 + 2.
Output: {{ "step": "analyse", "content": "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ "step": "think", "content": "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ "step": "output", "content": "4" }}
Output: {{ "step": "validate", "content": "seems like 4 is correct ans for 2 + 2" }}
Output: {{ "step": "result", "content": "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""
while True:
    messages = []

    user_input = input("Enter your query: ")
    if user_input.lower().strip() == "exit":
        print("Exiting the program.")
        break
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