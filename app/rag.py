import numpy as np
import os

os.environ['NUMPY_IMPORT'] = 'done'  # This ensures numpy is loaded

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from app.config import CHROMA_DB_DIR, EMBEDDING_MODEL
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document


from dotenv import load_dotenv
load_dotenv()
OPENAI_ROUTER_TOKEN=os.getenv("OPENROUTER")
HUGGINGFACETOEN=os.getenv("HUGGINGFACETOEN")
# Set a writable cache directory
os.environ["TRANSFORMERS_CACHE"] = "/tmp/.cache"
os.makedirs("/tmp/.cache", exist_ok=True)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"local_files_only": False})

# Chroma DB
db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)


def add_document(file_path: str, user_id: str):
    # Load file
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise RuntimeError(f"Unsupported file type: {file_path}")
    
    documents = loader.load()

    # Split into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Add metadata directly to Document objects
    docs_with_metadata = [
        Document(page_content=d.page_content, metadata={"user_id": user_id, "filename": os.path.basename(file_path)})
        for d in docs
    ]

    # Add to vector store
    db.add_documents(docs_with_metadata)


def get_qa_chain(user_id: str):
    """
    Return a RetrievalQA pipeline for a specific user using OpenRouter's Phi-3 Medium Instruct model.
    
    Args:
        user_id (str): Unique identifier for the user.
    """
    # Initialize LLM with OpenRouter
    llm = ChatOpenAI(
        openai_api_key=OPENAI_ROUTER_TOKEN,  # your OpenRouter API key
        model="meta-llama/llama-4-scout:free",       # free OpenRouter model
        temperature=0,
        max_tokens=512,
        openai_api_base="https://openrouter.ai/api/v1"  # OpenRouter endpoint
    )
    # Create retriever filtered by user_id
    retriever = db.as_retriever(search_kwargs={"filter": {"user_id": user_id}})

    # Build RetrievalQA pipeline
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    return qa



