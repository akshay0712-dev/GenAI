import os
from dotenv import load_dotenv
from google import genai
import json
import re
import random
import requests
import socket
import subprocess
import uuid
from google.genai import types
from datetime import datetime

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Function to safely extract JSON from text
def safe_json_extract(text):
    try:
        return [json.loads(text)]
    except json.JSONDecodeError:
        blocks = re.findall(r'{[^{}]*}', text, re.DOTALL)
        valid_blocks = []
        for block in blocks:
            try:
                valid_blocks.append(json.loads(block))
            except:
                continue
        return valid_blocks

# Tool

#  Function to run system commands
def run_commands(command: str):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output}"

available_tools = {
    "run_commands": {
        "fn": run_commands,
        "description": "Runs a system command and returns the result."
    }
}


# Generate system prompt with available tools
tool_descriptions = "\n".join(
    [f"- {name}: {info['description']}" for name, info in available_tools.items()]
)
print (f"Available Tools:\n{tool_descriptions}")
# System prompt
system_prompt = f"""
You are a helpful AI Assistant who is specialized in resolving user queries.
You work on start, plan, action, observe, and output steps.
For the given user query and available tools, plan the step-by-step execution.
Based on the planning, select the relevant tool from the available tool.
If the tool is not available than try to resolve the query using your knowledge.
Then, perform an action to call the tool.
Wait for the observation, and based on the observation, resolve the user query.

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyze the user query.

Output JSON Format:
{{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input parameter for the function"
}}

Available Tools:
{tool_descriptions}



Example:
    User Query:   In which directory am i working show all the files and folders in it 
    Output: {{ "step": "plan", "content": "The user is intrested to know their current working directory and all the files inside it" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call run_commands to run pwd first" }}
    Output: {{ "step": "action", "function": "run_commands", "input": "pwd" }}
    Output: {{ "step": "observe", "output": "/c/Users/aksha/Desktop/CODE/GenAI/AI Agent" }}
    Output: {{ "step": "plan", "content": "for listing all the files and folders inside working directory i should run ls -la" }}
    Output: {{ "step": "action", "function": "run_commands", "input": "ls -la" }}
    Output: {{ "step": "observe", "output": "-rw-r--r-- 1 aksha 197609    27 May 31 09:29 .dockerignore -rw-r--r-- 1 aksha 197609   104 May 31 23:54 .env" }}
    Output: {{ "step": "output", "content": "User is workin in directory c/Users/aksha/Desktop/CODE/GenAI/AI Agent. all files and folders inside it are .dockerignore .env  " }}

Do not return a JSON block inside the 'content' string. The 'content' should only be a plain text description or result.

"""

# Start conversation
print("Welcome to the AI Agent! Type 'exit' to quit.")
while True:
    
    user_query = input("Enter your query >  ")
    if user_query.lower().strip() == "exit" or user_query.lower().strip() == "quit":
        print("Exiting the program.")
        break
    messages = [f"User Query: {user_query}"]

    finished = False
    while not finished:
        # Generate next step
        response = client.models.generate_content(
            contents="\n".join(messages),
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2  # More deterministic
            )
        )

        # Clean Gemini output
        clean_text = response.text.strip()
        clean_text = clean_text.replace("```json", "").replace("```", "").strip()
        if clean_text.startswith("{{") and clean_text.endswith("}}"):
            clean_text = clean_text[1:-1].strip()

        json_blocks = safe_json_extract(clean_text)

        for parsed_response  in json_blocks:
           

            step = parsed_response.get("step")
            print(f"🔁 Step: {step} → {parsed_response.get('content')}")

            # Append to conversation
            messages.append(json.dumps(parsed_response))

            if step == "action":
                tool_name = parsed_response.get("function")
                print(f"🔧 Action: Calling tool '{tool_name}' with input: {parsed_response.get('input')}")
                if tool_name in available_tools:
                    result = available_tools[tool_name]["fn"](parsed_response["input"])
                    print(f"✅ Tool Result: {result}")
                    observation = {
                        "step": "observe",
                        "output": result
                    }
                    messages.append(json.dumps(observation))


            if step == "output":
                print(f"\n✅ Final Answer: {parsed_response.get('content')}")
                finished = True
                break
        if step == "output":
            break


      
