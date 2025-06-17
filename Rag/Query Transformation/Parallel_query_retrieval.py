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
import ast 
from concurrent.futures import ThreadPoolExecutor
import threading
import time


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
- Use the context above to answer the question as accurately and descriptively as possible.
- Do not use any outside knowledge or assumptions beyond what is given in the context.
- Add a summery of your answer at the last
- If the context does not provide enough information to answer the question, respond with:
"I don't know as the context is insufficient."


Guidelines:
- Format your answer for terminal display using ANSI escape codes:
    - Use bright colors to highlight keywords and examples.
    - Use bold or underline for headings.
    - Use proper indentation and spacing for readability.

Precaution: 
- before giving the answer rechake if answer is complete and propery forated and used Used bright colors to highlight keywords and examples using ANSI escape codes
"""

# Sends the prompt and user question to the GenAI model and returns the response
def answer_question(client, prompt, question):
    print("answer_question is called")
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            max_output_tokens=1000,
            temperature=0.1,  # Low temperature for more deterministic results
        ),
        contents=question,
    )
    return response.text  # Returns the text of the AI-generated answer

def context_texts(question, client, retriever):
    system_prompt = f"""
You are an intelligent and helpful assistant. Your task is to take a user's question and generate thirty distinct, relevant search queries that capture different possible interpretations or aspects of the original query.

Guidelines:
- Rephrase the original query to cover slightly different angles or subtopics.
- Avoid repeating the exact same wording.
- Ensure all generated queries remain closely tied to the user's original intent.
- Do not include the original query in the output.

Strict Guideline:
- Before giving result rechake the output formate

User Question: {question}

Format:
Return the three queries as a valid Python-style list of strings, like: ["query1", "query2", "query3", .....]

Example:
If the user question is: "How does Node.js handle file operations?"
You might respond with:
["What is the role of the fs module in Node.js?", "How to read and write files using Node.js?", "Node.js methods for file manipulation",.......]

Only generate the list of thirty queries.
"""

    # Ask model to create alternate queries
    multi_query = answer_question(client, system_prompt, question)
    if multi_query.startswith("```"):
        multi_query = multi_query.strip("`")  # remove backticks
        # Optionally remove leading language label (like "python")
        if multi_query.lower().startswith("python"):
            multi_query = multi_query[len("python"):].strip()
    try:
        parsed_queries = ast.literal_eval(multi_query.strip())
        if not isinstance(parsed_queries, list) or not all(isinstance(q, str) for q in parsed_queries):
            raise ValueError("Parsed result is not a valid list of strings.")

    except (SyntaxError, ValueError):
        print("❌ Could not parse the generated queries.")
        print(f"Raw output: {multi_query}")
        return ""

    seen = set()
    unique_chunks = []
    lock = threading.Lock()

    def process_query(query):
        print(f"🔍 Query -> {query}")
        search_results = retriever.similarity_search(query=query)
        added = 0
        with lock:
            for chunk in search_results:
                if chunk.page_content not in seen:
                    seen.add(chunk.page_content)
                    unique_chunks.append(chunk)
                    added += 1
        print(f"✅ Added {added} chunks from '{query}'")

    # Run all queries in parallel
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(process_query, parsed_queries)
    end_time = time.time()

    print(f"\n⏱️ Parallel similarity search took: {end_time - start_time:.2f} seconds")
    print(f"\n📦 Total unique chunks collected: {len(unique_chunks)}")

    context_text = "\n\n".join(chunk.page_content for chunk in unique_chunks)
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

    print_colored_answer(response)   # Output the answer to the console

# Entry point for the script
if __name__ == "__main__":
    main()
