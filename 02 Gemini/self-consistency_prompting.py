from dotenv import load_dotenv
import os
import json
from google import genai
from collections import Counter

# Load .env variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Set API key directly to genai
genai.configure(api_key=api_key)  # <-- only works if you're using the correct package

# OR if `configure` gives an error, do this instead:
# os.environ["GOOGLE_API_KEY"] = api_key

# Choose the model (1.5 flash or 1.5 pro)
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"

# Self-consistency function
def self_consistent_answer(prompt, n=10, temperature=0.9):
    responses = []

    for _ in range(n):
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                top_k=40,
                top_p=0.95
            )
        )
        text = response.text.strip()
        responses.append(text)

    # Show all responses
    print("\nAll responses:\n")
    for i, res in enumerate(responses):
        print(f"[{i+1}] {res}\n")

    # Majority voting
    counter = Counter(responses)
    most_common, count = counter.most_common(1)[0]

    print(f"\n🧠 Most consistent answer (appeared {count}/{n} times):\n{most_common}")
    return most_common

# Example use
prompt = "If there are 5 houses and each house has 5 rooms, and each room has 5 chairs, how many chairs are there in total?"
self_consistent_answer(prompt)
