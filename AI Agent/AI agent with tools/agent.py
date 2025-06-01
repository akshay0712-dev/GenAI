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
# Weather Agent that uses Gemini to search Wikipedia and fetch weather information
def get_weather(city: str):
    print(f"🌤️ Fetching weather for {city}")
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is: {response.text.strip()}"
    return "Something went wrong, please try again later." if "Error" in response.text else response.text.strip()


# Tool for searching Wikipedia
def search_wikipedia(query: str):
    print(f"🔍 Searching Wikipedia for: {query}")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary found.")
    return "Failed to fetch Wikipedia summary."

# Tool for defining a word
def define_word(word : str):
    print(f"📖 Defining word: {word}")
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return f"Definition of '{word}': {meaning}"
        except (KeyError, IndexError, TypeError):
            return f"⚠️ Could not extract a definition for '{word}' from the API response."
    elif response.status_code == 404:
        return f"❌ No definitions found for '{word}'."
    else:
        return f"🚨 Error fetching definition for '{word}': HTTP {response.status_code} {response}"



# Function to get today's date
def get_today_date(text : str):
    print(f"📅 Fetching today's date {text}")
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y.")

# Tool for rolling a dice
def roll_dice(text : str):
    return f"🎲 You rolled a {random.randint(1, 6)}!"

# Tool for telling a joke
def tell_joke(text : str):
    print("😂 Fetching a joke...")
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['setup']} 😂 {data['punchline']}"
        return "Couldn't fetch a joke at the moment."
    except Exception as e:
        return f"Something went wrong while fetching the joke: {str(e)}"

# Tool to get public IP information
def get_ip_info(text : str):
    return f"Your public IP info: {requests.get('https://api.ipify.org').text}"

# Tool to ping a website and get its IP address
def ping_website(url: str):
    domain = re.sub(r'^https?://', '', url).strip().split('/')[0]
    try:
        host = socket.gethostbyname(domain)
        return f"The IP address of {domain} is {host}"
    except Exception:
        return "Could not resolve the website."

# Tool to generate a UUID
def generate_uuid(text : str):
    return f"Generated UUID: {str(uuid.uuid4())}"


# Tool to get latest news
def get_latest_news(query: str = None):
    print(f"📰 Fetching news for query: {query if query else 'Top Headlines'}")
    
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        return "Error: NEWS_API_KEY not found in environment variables. Please set it to use this feature."

    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us"
    }
    if query:
        params["q"] = query

    headers = {'X-Api-Key': news_api_key} 
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                return "No news found for your query."
            
            formatted_news = []
            for article in articles[:5]: # Get top 3-5 articles
                title = article.get('title', 'No Title')
                description = article.get('description', '')
                url = article.get('url', '')
                news_item = f"Title: {title}"
                if description:
                    news_item += f"\n  Description: {description}"
                news_item += f"\n  URL: {url}"
                formatted_news.append(news_item)
            return "\n\n".join(formatted_news)
        else:
            # It's good to include the response text for more detailed error diagnosis
            error_detail = response.text
            try:
                # Attempt to parse JSON error from NewsAPI for better readability
                json_error = response.json()
                if 'message' in json_error:
                    error_detail = json_error['message']
            except json.JSONDecodeError:
                pass # Stick with response.text if not JSON
            return f"Failed to fetch news. Status code: {response.status_code} - {error_detail}"
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch news. Error: {e}"
    

#  Function to run system commands
def run_commands(command: str):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output}"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes the city name as a input and returns the current weather in that city.",
    },
    "search_wikipedia": {
        "fn": search_wikipedia,
        "description": "Searches Wikipedia for the given query and returns a summary.",
    },
    "define_word": {
        "fn": define_word,
        "description": "Takes a word as input and returns its definition.",
    },
    "get_today_date": {
    "fn": get_today_date,
    "description": "Returns todays date only",
    },
    "roll_dice": {
        "fn": roll_dice, 
        "description": "Rolls a 6-sided dice."
    },
    "tell_joke": {
    "fn": tell_joke,
    "description": "Fetches and returns a random joke.",
    },
    "get_ip_info": {
        "fn": get_ip_info, 
        "description": "Fetches your public IP address."
    },
    "ping_website": {
        "fn": ping_website, 
        "description": "Resolves a website's IP address."
    },
    "generate_uuid": {
        "fn": generate_uuid, 
        "description": "Generates a UUID."
    },
    "get_latest_news": {
        "fn": get_latest_news,
        "description": "Fetches the latest news headlines. Optionally takes a query to search for specific news topics."
    },
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
    User Query:  What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Celcius" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

Do not return a JSON block inside the 'content' string. The 'content' should only be a plain text description or result.

"""

# Start conversation
print("Welcome to the AI Agent! Type 'exit' to quit.") 
history = []
while True:
    
    user_query = input("Enter your query >  ")
    if user_query.lower().strip() == "exit" or user_query.lower().strip() == "quit":
        print("Exiting the program.")
        break
    # Build conversation history string
    history_string = "\n".join([
        f"User: {entry['query']}\nAssistant: {entry['response']}" for entry in history
    ])

    # Include history and the new user query
    messages = [f"{history_string}\nUser: {user_query}"]

    

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
                assistant_response = parsed_response.get("content")
                print(f"\n✅ Final Answer: {assistant_response}")
                history.append({
                    "query": user_query,
                    "response": assistant_response
                })
                finished = True
                break
        if step == "output":
            break


      
# print(f"\nConversation History: {json.dumps(history, indent=2)}")
print("\n Conversation History:")
for entry in history:
    print(f"User: {entry['query']}\nAssistant: {entry['response']}\n")