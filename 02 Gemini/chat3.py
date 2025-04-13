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


response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents = types.Content(
  role='user', parts=[types.Part.from_text(text='Why is the sky blue?')]
    # role='user', parts=[types.Part.from_text(text= json.dumps({"step": "analyse","content": "The user is asking a question about a natural phenomenon, specifically the reason for the sky's blue color. This requires an explanation based on scientific principles."}))]
    # role='user', parts=[types.Part.from_text(text= json.dumps({ "step": "think", "content": "The blue color of the sky is due to a phenomenon called Rayleigh scattering. I need to explain this concept in a clear and concise manner, avoiding overly technical jargon." }  ))]
    # role='user', parts=[types.Part.from_text(text= json.dumps({"step": "analyse","content": "The user wants an explanation of Rayleigh scattering, which is responsible for the sky's blue color. The explanation should be easy to understand."} ))]
    # role='user', parts=[types.Part.from_text(text= json.dumps({ "step": "think", "content": "Okay, I need to explain Rayleigh scattering in a simple way, focusing on why it makes the sky blue. I should avoid overly technical terms and use analogies if possible. Here's my plan: 1. Briefly define Rayleigh scattering. 2. Explain how sunlight interacts with air molecules. 3. Describe why blue light is scattered more than other colors. 4. Relate this scattering to the color we see in the sky. 5. Briefly mention why sunsets are reddish." } ))]
    ),
    config=types.GenerateContentConfig(
        system_instruction= system_prompt,
        max_output_tokens=1000,
        temperature=0.1,

    ),
)
print(response.text)