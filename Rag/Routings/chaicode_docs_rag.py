from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import ast 
from concurrent.futures import ThreadPoolExecutor
import threading
import time

data_bases = [
    {"html": "HTML (HyperText Markup Language) is the standard markup language used to structure and display content on the web."},
    {"git": "Git is a distributed version control system used for tracking changes in source code and coordinating work among developers."},
    {"c": "C++ is a powerful general-purpose programming language that supports object-oriented, procedural, and generic programming features."},
    {"django": "Django is a high-level Python web framework that promotes rapid development and clean, pragmatic design of web applications."},
    {"sql": "SQL (Structured Query Language) is used to communicate with and manage data in relational databases through queries, updates, and data definition."},
    {"devops": "DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle and deliver high-quality software continuously."}
]

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

def print_colored_answer(answer):
    print(f"\n{Style.BOLD}{Style.CYAN}📘 Answer:{Style.RESET}\n")

    # Clean output by decoding escape sequences
    if answer.startswith("```") and "```" in answer[3:]:
        # Remove code block markers
        answer = answer.strip("`").strip("text").strip()
    
    # Interpret ANSI codes
    interpreted_answer = answer.encode().decode("unicode_escape")
    
    print(interpreted_answer + Style.RESET)

def load_api_key():
    # print("load_api_key is called")
    load_dotenv()  # Load environment variables from .env file
    return os.getenv("API_KEY")  # Return the API key

def initialize_genai_client(api_key):
    # print("initialize_genai_client is called")
    return genai.Client(api_key=api_key)

def topic_links() :
    BASE_INDEX = "https://docs.chaicode.com/youtube/getting-started/"
    BASE_DOCS = "https://docs.chaicode.com"
    def get_all_links_from_page(url):
        """Fetch all absolute URLs from a given page."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = {
                urljoin(BASE_DOCS, a['href'])
                for a in soup.find_all('a', href=True)
                if a['href'].startswith('/youtube/chai-aur-')  # Ensure relevant links only
            }
            return list(links)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []

    def group_links_by_topic(welcome_links):
        """From welcome links, extract topics and gather full lesson links per topic."""
        topic_urls = defaultdict(list)

        for welcome_url in welcome_links:
            # Get topic root: remove '/welcome/' from the end
            if not welcome_url.endswith('/welcome/'):
                continue
            topic_base = welcome_url.rsplit('welcome/', 1)[0]
            topic_slug = topic_base.strip("/").split("/")[-1]  # e.g., chai-aur-html
            topic = topic_slug.replace("chai-aur-", "")

            # Fetch lesson links under this topic
            topic_lessons = get_all_links_from_page(welcome_url)
            # Filter only links starting with the base (e.g., chai-aur-html/)
            full_lesson_links = [
                link for link in topic_lessons if link.startswith(topic_base)
            ]

            topic_urls[topic] = sorted(set(full_lesson_links))  # Deduplicate + sort

        return dict(topic_urls)

    # === Main ===
    welcome_links = get_all_links_from_page(BASE_INDEX)
    topic_urls = group_links_by_topic(welcome_links)
    return(topic_urls)

def answer_question(client, prompt, question):
    # print("answer_question is called")
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            max_output_tokens=1000,
            temperature=0.1,  # Low temperature for more deterministic results
        ),
        contents=question,
    )
    return response.text

# fetching data from url and embadding in vector store
def embedding(embeddings):
    topic_urls = topic_links()
    # Output or use it
    for topic, urls in topic_urls.items():
        
        print(f"\n📚 {topic.upper()} ({len(urls)} lessons)")
        def process_url(url):
            start_time = time.time()
            print(f" => 📚 {topic.upper()} : {url}")
            
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            extracted_text = soup.get_text(separator="\n")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            ) 

            split_docs = text_splitter.create_documents([extracted_text], metadatas=[{"source": url, "topic": topic}])
            # print(f"Number of split documents for {url.replace(f"https://docs.chaicode.com/youtube/chai-aur-{topic.lower()}/","").replace("/","").replace("-"," ")} : {len(split_docs)}")

            

            vector_store = QdrantVectorStore.from_documents(
                documents=[],
                url="http://localhost:6333",
                collection_name=topic,
                embedding=embeddings
            )
            vector_store.add_documents(documents=split_docs)
            end_time = time.time()
            print(f"Number of split documents for {url.replace(f"https://docs.chaicode.com/youtube/chai-aur-{topic.lower()}/","").replace("/","").replace("-"," ")} : {len(split_docs)}, Time: {end_time - start_time:.2f} seconds ")
       
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            executor.map(process_url, urls)
        end_time = time.time()
        print(f"\n⏱️ Parallel url injestion for {topic} took: {end_time - start_time:.2f} seconds")



    print("Injestion done. ")

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
- If the context does not provide enough information to answer the question, respond with: "I don't know as the context is insufficient."
- At the top of the answer give all the Source Url


Guidelines:
- Format your answer for terminal display using ANSI escape codes:
    - Use bright colors to highlight keywords and examples.
    - Use bold or underline for headings.
    - Use proper indentation and spacing for readability.
- must give the source 

Precaution: 
- before giving the answer rechake if answer is complete and propery formated and used Used bright colors to highlight keywords and examples using ANSI escape codes and also check if the correct source url is give
"""

def generate_collection_prompt(data_bases) :
    return f"""
You are an intelligent and helpful assistant tasked with routing toward best database matches

Context:
{data_bases}

Instructions:
- you are given a list of data bases name and the description about data bases. Your task is to return the list of name of most relevant data base
- Only return the list of name of data base as a valid python string

Example:
User Query: backed can be nade using
Answer: ["node js", "python"]
User Query: socket io
Answer: ["node js"]
"""

def get_retriever(embeddings, collection_name):
    # print("get_retriever is called")
    return QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embeddings
    )

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
        # print(f"🔍 Query -> {query}")
        search_results = retriever.similarity_search(query=query)
        added = 0
        with lock:
            for chunk in search_results:
                if chunk.page_content not in seen:
                    seen.add(chunk.page_content)
                    unique_chunks.append(chunk)
                    added += 1
        # print(f"✅ Added {added} chunks from '{query}'")

    # Run all queries in parallel
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(process_query, parsed_queries)
    end_time = time.time()

    print(f"\n⏱️ Parallel similarity search took: {end_time - start_time:.2f} seconds")
    print(f"\n📦 Total unique chunks collected: {len(unique_chunks)}")

    # print(f"Unique chunks: {unique_chunks}")

    context_text = "\n\n".join(
        f"Source: {chunk.metadata['source']}\nContent:\n{chunk.page_content}"
        for chunk in unique_chunks)
    return context_text


# Main execution flow
def main():
    # print("main is called")
    api_key = load_api_key()  # Load API key from environment
    client = initialize_genai_client(api_key)  # Initialize GenAI client
    os.environ["GOOGLE_API_KEY"] = load_api_key()
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=os.environ["GOOGLE_API_KEY"],
    )
    embedding(embeddings)

    while True:
        print(f"\n{Style.YELLOW}Enter {Style.BOLD}'exit'{Style.RESET}{Style.YELLOW} to EXIT.{Style.RESET}")
        question = input(f"{Style.BOLD}{Style.BLUE}❓ Enter your question: {Style.RESET}") # Prompt user for a question

        if question.strip().lower() == "exit":
            print(f"\n{Style.GREEN}👋 Exiting...{Style.RESET}")
            break
   

        get_collection_prompt = generate_collection_prompt(data_bases)
        
        collection_name =  answer_question(client, get_collection_prompt, question) 
        # print(f"Collection list: {collection_name}")
        if isinstance(collection_name, str):
            collection_name = collection_name.strip("[]").replace("'", "").replace('"', "").replace("```python","").replace("```","").replace("\n","").replace("[","").replace("]","").split(", ")

        # print(f"Collection list: {collection_name}")
        context_text = ""

        # print(f"Collection list: {collection_name}")
        def process_collection(collection):
            print(f"Searching from {Style.BOLD}{Style.YELLOW}{collection.upper()}{Style.RESET} docs..")
            collection = collection.lower()
            retriever = get_retriever(embeddings, collection)
            return context_texts(question, client, retriever)
        

        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            results = executor.map(process_collection, collection_name)
        end_time = time.time()


        print(f"\n⏱️ Parallel context find took: {end_time - start_time:.2f} seconds")
        # print(f"Result: {results}")
        context_text = "\n".join(results)
        # print(f"Context text: {context_text}")

        system_prompt_answer = generate_prompt(context_text)  # Generate prompt using context chunks
        response = answer_question(client, system_prompt_answer, question)  # Get AI-generated answer

        # print(response)
        print_colored_answer(response) 



# Entry point for the script
if __name__ == "__main__":
    main()
