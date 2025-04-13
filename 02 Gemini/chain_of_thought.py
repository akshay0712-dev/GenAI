from dotenv import load_dotenv
import os
import json
from google import genai
from google.genai import types

load_dotenv() 
api_key = os.getenv("API_KEY")
# Only run this block for Gemini Developer API
client = genai.Client(api_key = api_key)

# Start a new chat session
chat = client.chats.create(model='gemini-2.0-flash') 

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
1. Follow the strict steps analyse -> think -> output -> validate -> result .
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2.
# Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

# Set the system prompt
chat.send_message(system_prompt)

# Get initial user query
query = input("> ")
chat.send_message(query)

completed_steps = set()

while True:
    response = chat.send_message("continue")
    raw = response.text.strip()

    # Remove markdown code block if present
    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed_response = json.loads(raw)
    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Full response:\n", response.text)
        break

    step = parsed_response.get("step")
    content = parsed_response.get("content")

    if not step or not content:
        print("⚠️ Missing 'step' or 'content' in response.")
        break

    completed_steps.add(step)

   

    print(f"🧠 [{step}]: {content}")

    # Exit loop after reaching final step
    if step == "result":
        break

