from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import VECTOR_STORE_DIR
from app.indexing.embedding import get_embedding_model

def build_vector_store(chunks: list[Document]) -> FAISS:
    if not chunks:
        raise ValueError("Chunks list cannot be empty")

    embedding_model = get_embedding_model()
    return FAISS.from_documents(
        chunks,
        embedding_model,
    )

def save_vector_store(vector_store: FAISS, session_id: str) -> Path:
    save_path = VECTOR_STORE_DIR / session_id
    save_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(save_path)
    return save_path

def load_vector_store(session_id: str) -> FAISS:
    load_path = VECTOR_STORE_DIR / session_id
    embedding_model = get_embedding_model()

    return FAISS.load_local(
        str(load_path),
        embedding_model,
        allow_dangerous_deserialization = True,
    )


def create_retriever(vector_store: FAISS, k:int = 10):
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":k,
            "fetch_k": 40,
        }
    )






