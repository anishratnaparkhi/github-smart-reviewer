from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import GOOGLE_API_KEY, LLM_PROVIDER, GEMINI_EMBEDDING_MODEL

class EmbeddingConfigError(Exception):
    pass

def get_embedding_model():
    if LLM_PROVIDER == "google":
        if not GOOGLE_API_KEY:
            raise EmbeddingConfigError("GOOGLE_API_KEY is missing in .env")
        
        return GoogleGenerativeAIEmbeddings(
            model = GEMINI_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,
        )

    raise EmbeddingConfigError("Enter a valid LLM provider in .env")

