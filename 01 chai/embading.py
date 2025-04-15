from google import genai
import os

# api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key="AIzaSyAKPsVOicq0wsLJjEVrtVQNg_eEu_5z_8Q")

text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

response = client.models.embed_content(
    model = "gemini-embedding-exp-03-07",
    contents = text
)

print("Vector Embeddings : ", response.embeddings)