from app.indexing.vector_store import (
    build_vector_store,
    create_retriever,
    save_vector_store,
)
from langchain_core.documents import Document

def prepare_vector_store_and_retriever(chunks, session_id: str) -> dict:
    vector_store = build_vector_store(chunks)
    vector_store_path = save_vector_store(vector_store, session_id)
    retriever = create_retriever(vector_store)

    return {
        "vector_store": vector_store,
        "vector_store_path": vector_store_path,
        "retriever": retriever,
    }

def retrieve_relevant_chunks(retriever, query:str) -> list[Document]:
    return retriever.invoke(query)
