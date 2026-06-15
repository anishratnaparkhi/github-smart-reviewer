from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY, LLM_PROVIDER, GEMINI_MODEL

class LLMConfigError(Exception):
    pass

def get_chat_model():
    if LLM_PROVIDER == "google":
        if not GOOGLE_API_KEY:
            raise LLMConfigError("GOOGLE_API_KEY is missing in .env.")
    
        return ChatGoogleGenerativeAI(
            model  = GEMINI_MODEL,
            google_api_key = GOOGLE_API_KEY,
            temperature = 0.2,
            max_retries = 5,
        )
    
    raise LLMConfigError("Invalid llm provider.")

