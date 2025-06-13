from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai
from google.genai import types
from langchain_core.documents import Document
from dotenv import load_dotenv
from pathlib import Path
import os

# ----------- Function Definitions -----------

def load_environment():
    print("🔧 Function called: load_environment")
    load_dotenv()
    return os.getenv("API_KEY")

def load_script(video_id: str) -> str:
    print("🎬 Function called: load_script")

    # Define preferred language order: English, then Hindi
    preferred_languages = ['en', 'hi']

    for lang in preferred_languages:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            full_text = " ".join([t["text"] for t in transcript])
            print(f"✅ Transcript loaded in language: {lang}")
            print(f"Transcript: {full_text} \n")
            return full_text
        except NoTranscriptFound:
            print(f"⚠️ No transcript found in language: {lang}")
        except Exception as e:
            print(f"❌ Error while loading transcript in {lang}: {e}")
    
    print("❌ No transcript could be loaded in preferred languages.")
    return ""


def wrap_text_as_document(text: str):
    print("📄 Function called: wrap_text_as_document")
    return [Document(page_content=text)]


def split_documents(docs, chunk_size=3000, chunk_overlap=500):
    print("✂️  Function called: split_documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)


def setup_embeddings():
    print("🔗 Function called: setup_embeddings")
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=os.getenv("GOOGLE_API_KEY")
    )


def ingest_documents_to_qdrant(split_docs, embeddings, collection_name):
    print("📦 Function called: ingest_documents_to_qdrant")
    vector_store = QdrantVectorStore.from_documents(
        documents=split_docs,
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embeddings
    )
    return vector_store


def get_retriever(embeddings, collection_name):
    print("🔍 Function called: get_retriever")
    return QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embeddings
    )


def build_system_prompt(context):
    print("🧠 Function called: build_system_prompt")
    return f"""
You are an intelligent and helpful assistant tasked with answering questions using only the provided context.

Context:
{context}

Instructions:
- Use the context above to answer the question as accurately and descriptively as possible.
- You can use extra information related to context to answer the question. Like from your knowladge u can expand the answer in more detail.

"""


def generate_answer(client, question, system_prompt):
    print("🤖 Function called: generate_answer")
    return client.models.generate_content(
        model='gemini-2.0-flash-001',
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=2000,
            temperature=0.1,
        ),
        contents=question,
    )

# ----------- Main Execution -----------

if __name__ == "__main__":
    api_key = load_environment()
    os.environ["GOOGLE_API_KEY"] = api_key
    client = genai.Client(api_key=api_key)

    # video_id = input("Enter video ID: ") #"AHMEtNAZTP4"
    # script_text = load_script(video_id)
    
    # if not script_text:
    #     print("❌ No script loaded. Exiting.")
    #     exit()

    # documents = wrap_text_as_document(script_text)
    # split_docs = split_documents(documents)
    embeddings = setup_embeddings()

    # ingest_documents_to_qdrant(split_docs, embeddings, "YouTube_Script")
    retriever = get_retriever(embeddings, "YouTube_Script")

    question = input("Enter your question: ")
    search_result = retriever.similarity_search(query=question)
    system_prompt = build_system_prompt(search_result)

    response = generate_answer(client, question, system_prompt)
    print("\n📌 Answer:\n", response.text)
