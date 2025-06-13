from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import getpass
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key = API_KEY)


# pdf_path = Path(__file__).parent  / "nodejs.pdf"
# print(pdf_path.exists()) 
# print(f"Loading PDF from: {pdf_path}")

# loader = PyPDFLoader(file_path=pdf_path)
# docs = loader.load()
# # print(docs[45])


# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000, 
#     chunk_overlap=200
# )

# split_docs = text_splitter.split_documents(documents=docs)

# print(f"Number of original documents: {len(docs)}")
# print(f"Number of split documents: {len(split_docs)}")

# print(split_docs[117])


os.environ["GOOGLE_API_KEY"] = API_KEY

embeddings = GoogleGenerativeAIEmbeddings(
  model="models/embedding-001",
  api_key=os.environ["GOOGLE_API_KEY"],
)

# print("Generating embeddings...",embeddings)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embeddings
# )

# vector_store.add_documents(documents=split_docs)
print("Injestion done. ")

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embeddings
)


# print(f"Revelent chunks: {search_result}")
question = input("Enter your question: ")

search_result = retriver.similarity_search(
    query=question,
)
SYSTEM_PROMPT = f"""
You are an intelligent and helpful assistant tasked with answering questions using only the provided context.

Context:
{search_result}

Instructions:
- Use the context above to answer the question as accurately and descriptive as possible.
- Do not use any outside knowledge or assumptions beyond what is given in the context.
- If the context does not provide enough information to answer the question, respond with:
"I don't know as the context is insufficient."
"""


response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    config=types.GenerateContentConfig(
        system_instruction= SYSTEM_PROMPT,
        max_output_tokens=1000,
        temperature=0.1,
    ),
    contents= question,
)
print(response.text)