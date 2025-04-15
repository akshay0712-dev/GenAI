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
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

content = [
    'what is 3 + 4 * 5',
    json.dumps({
        "step": "analyse",
        "content": "The user is asking to evaluate the expression 3 + 4 * 5. This involves addition and multiplication."
    }),
    json.dumps({
        "step": "think",
        "content": "I need to remember the order of operations (PEMDAS/BODMAS). Multiplication comes before addition. So, I'll multiply 4 and 5 first, then add the result to 3."
    }),
    json.dumps({
        "step": "output",
        "content": "Following the order of operations, 4 * 5 = 20. Then, 3 + 20 = 23."
    }),
    json.dumps({
        "step": "validate",
        "content": "Let's re-check the calculation. 4 multiplied by 5 is indeed 20. Adding 3 to 20 gives 23. The order of operations was correctly applied."
    }),
]

print(f'contents:    {content}') 

# Add one more step to the list
content.append(
    json.dumps({
        "step": "result",
        "content": "3 + 4 * 5 = 23, calculated by first multiplying 4 and 5, and then adding 3 to the result."
    })
)

print(f'updated contents:    {content}') 


response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents = content,
    config=types.GenerateContentConfig(
        system_instruction= system_prompt,
        max_output_tokens=1000,
        temperature=0.1,

    ),
   
)
print(response.text)