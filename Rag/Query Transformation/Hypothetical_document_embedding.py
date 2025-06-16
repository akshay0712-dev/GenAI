# Import necessary libraries
import os
from pathlib import Path
from dotenv import load_dotenv  # Loads environment variables from a .env file
from langchain_community.document_loaders import PyPDFLoader  # Loads and parses PDF files
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Splits documents into chunks
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # For Google Generative AI embeddings
from langchain_qdrant import QdrantVectorStore  # Vector store interface for Qdrant
from google import genai  # Google's generative AI client
from google.genai import types  # Types for model configuration

# Define terminal style helpers
class Style:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GRAY = '\033[90m'

# Loads API key from environment variable
def load_api_key():
    print("load_api_key is called")
    load_dotenv()  # Load environment variables from .env file
    return os.getenv("API_KEY")  # Return the API key

# Initializes the GenAI client using the provided API key
def initialize_genai_client(api_key):
    print("initialize_genai_client is called")
    return genai.Client(api_key=api_key)

# Loads PDF from the specified path
def load_pdf(file_name: str):
    print("load_pdf is called")
    pdf_path = Path(__file__).parent / file_name
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found at path: {pdf_path}")
    print(f"Loading PDF from: {pdf_path}")
    loader = PyPDFLoader(file_path=pdf_path)
    return loader.load()  # Returns the parsed PDF content as documents

# Splits large documents into smaller chunks for easier processing
def split_documents(docs, chunk_size=1000, chunk_overlap=200):
    print("split_documents is called")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents=docs)

# Sets up Google Generative AI embeddings model
def setup_embeddings(api_key):
    print("setup_embeddings is called")
    os.environ["GOOGLE_API_KEY"] = api_key  # Required for the embeddings API
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=api_key
    )

# Initializes a Qdrant vector store with the documents and embeddings
def initialize_vector_store(embeddings, collection_name="learning_langchain", documents=None):
    print("initialize_vector_store is called")
    vector_store = QdrantVectorStore.from_documents(
        documents=documents or [],  # Defaults to empty list if no documents
        url="http://localhost:6333",  # Local Qdrant instance
        collection_name=collection_name,
        embedding=embeddings
    )
    return vector_store

# Adds split documents into the vector store for future retrieval
def ingest_documents(vector_store, split_docs):
    print("ingest_documents is called")
    vector_store.add_documents(documents=split_docs)
    print("Ingestion done.")

# Retrieves the vector store for querying based on existing embeddings
def get_retriever(embeddings, collection_name="learning_langchain"):
    print("get_retriever is called")
    return QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embeddings
    )

# Generates a system instruction prompt using the context from similar documents
def generate_prompt(context_text):
   
    # print(f"Context text for prompt:\n{context_text}...")  # Debugging output to see context text
    
    return f"""
You are an intelligent and helpful assistant tasked with answering questions using only the provided context.

Context:
{context_text}

Instructions:
- Your top priority is to use the information in the context to answer the question.
- You may use general knowledge **only to clarify or elaborate**, but you may not introduce facts not present in the context as core parts of the answer.
- If the context does not provide enough information to answer the question meaningfully, respond with:
"Context is insufficient."


Guidelines:
- Format your answer for terminal display using ANSI escape codes:
    - Use bright colors to highlight keywords and examples.
    - Use bold or underline for headings.
    - Use proper indentation and spacing for readability.

"""

# Sends the prompt and user question to the GenAI model and returns the response
def answer_question(client, prompt, question):
    print("answer_question is called")
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            max_output_tokens=1000,
            temperature=0.5,  # Low temperature for more deterministic results
        ),
        contents=question,
    )
    return response.text  # Returns the text of the AI-generated answer

def context_texts(question, client, retriever):
    system_prompt = f"""
You are an intelligent and helpful assistant. Your task is to take a user's question and generate a Hypothetical Document on the topic related to question given by user


Guidelines:
- Analyze the question and give a documented answer of the user query
- Write a detailed document of 500–600 words with multiple examples and explanations.


User Question: {question}

Format:
Return a text document as valid python string like "your solution"

Example:
If the user question is: "How does Node.js handle file operations?"
You might respond with:
"Node.js handles file operations using the built-in fs (File System) module. It provides both synchronous and asynchronous methods to interact with the file system—such.............."


respond a valid python string
"""

    # Ask model to create alternate queries
    hypothetical_query = answer_question(client, system_prompt, question)

    seen = set()
    unique_chunks = []

    search_results = retriever.similarity_search( query = hypothetical_query)
    added = 0
    for chunk in search_results:
        if chunk.page_content not in seen:
            seen.add(chunk.page_content)
            unique_chunks.append(chunk)
            added += 1
    print(f"✅ Added {added} chunks ")

   

    context_text = "\n\n".join(chunk.page_content for chunk in unique_chunks)

    # print(f"Hypothetical query: {hypothetical_query}")
    return context_text


def print_colored_answer(answer):
    print(f"\n{Style.BOLD}{Style.CYAN}📘 Answer:{Style.RESET}\n")

    # Clean output by decoding escape sequences
    if answer.startswith("```") and "```" in answer[3:]:
        # Remove code block markers
        answer = answer.strip("`").strip("text").strip()
    
    # Interpret ANSI codes
    interpreted_answer = answer.encode().decode("unicode_escape")
    
    print(interpreted_answer + Style.RESET)

# Main execution flow
def main():
    print("main is called")
    api_key = load_api_key()  # Load API key from environment
    client = initialize_genai_client(api_key)  # Initialize GenAI client
    
    # Optional: Uncomment the lines below to load and ingest a PDF
    # docs = load_pdf("syllabus.pdf")
    # split_docs = split_documents(docs)
    
    embeddings = setup_embeddings(api_key)  # Set up embeddings model

    # Optional: Uncomment the lines below to initialize and populate the vector store
    # vector_store = initialize_vector_store(embeddings, documents=split_docs)
    # ingest_documents(vector_store, split_docs)

    retriever = get_retriever(embeddings)  # Load retriever from existing Qdrant collection

    question = input("Enter your question: ")  # Prompt user for a question


    context_text = context_texts(question, client, retriever) # 
    



    system_prompt_answer = generate_prompt(context_text)  # Generate prompt using context chunks
    # print(f"System prompt :{system_prompt_answer}")
    response = answer_question(client, system_prompt_answer, question)  # Get AI-generated answer

    print_colored_answer(response)  # Output the answer to the console

# Entry point for the script
if __name__ == "__main__":
    main()
