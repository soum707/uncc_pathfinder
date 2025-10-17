import os
from dotenv import load_dotenv
load_dotenv()

# FAISS path
DB_FAISS_PATH = "vectorstore/db_faiss"

# Survey summarization model (short text)
SURVEY_LLM_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

# RAG generation model (longer reasoning)
RAG_LLM_MODEL = "deepseek-r1-distill-llama-70b"

# Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Number of FAISS results to retrieve
TOP_K = 3

