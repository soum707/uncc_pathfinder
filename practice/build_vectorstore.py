from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import DB_FAISS_PATH
from langchain import hub

from dotenv import load_dotenv
load_dotenv()

def load_pdfs(data_path="data/"):
    loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def create_chunks(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def build_faiss_index(chunks):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(DB_FAISS_PATH)
    return db

if __name__ == "__main__":
    docs = load_pdfs()
    chunks = create_chunks(docs)
    db = build_faiss_index(chunks)
    print(f"FAISS index created with {len(chunks)} chunks at {DB_FAISS_PATH}")
