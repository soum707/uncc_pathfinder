import os
from dotenv import load_dotenv
load_dotenv()

# FAISS path
DB_FAISS_PATH = "vectorstore/db_faiss"

# Survey summarization model (short text)
SURVEY_LLM_MODEL = "llama-3.1-8b-instant"

# RAG generation model (longer reasoning)
RAG_LLM_MODEL = "llama-3.3-70b-versatile"

# Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Number of FAISS results to retrieve
TOP_K = 5

