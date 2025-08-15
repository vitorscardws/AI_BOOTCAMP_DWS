import os
from dotenv import load_dotenv

load_dotenv()

# Paths
PDF_PATH = "app/docs/MAGIC_RULES.pdf"
PPTX_PATH = "app/docs/PRESENTATION.pptx"
CACHE_PATH_PDF = "app/docs/pdf_embeddings.pkl"
CACHE_PATH_PPTX = "app/docs/pptx_embeddings.pkl"
CHUNK_SIZE = 350

# APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

OPENAI_HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
GROQ_HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Models
OPENAI_MODEL = "gpt-4o-mini"
GROQ_MODEL = "llama-3.3-70b-versatile"
