from app.indexing.chunker import chunk_documents
from app.indexing.document_builder import build_document_from_scan

def prepare_documents_and_chunks(scan_result: dict) -> dict:
    documents = build_document_from_scan(scan_result)
    chunks = chunk_documents(documents)

    return {
        "document_count": len(documents),
        "chunk_count": len(chunks),
        "documents": documents,
        "chunks": chunks,
    }