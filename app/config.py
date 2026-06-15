from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_REPOS_DIR = BASE_DIR / "temp_repos"
REPORTS_DIR = BASE_DIR / "reports"
VECTOR_STORE_DIR = BASE_DIR / "vectorstores"

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")

