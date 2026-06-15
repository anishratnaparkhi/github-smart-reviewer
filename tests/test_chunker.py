from langchain_core.documents import Document

from app.indexing.chunker import chunk_documents


def test_chunk_documents_creates_chunks():
    document = Document(
        page_content="hello world\n" * 500,
        metadata={
            "file_path": "main.py",
            "language": "Python",
        },
    )

    chunks = chunk_documents(
        documents=[document],
        chunk_size=200,
        chunk_overlap=50,
    )

    assert len(chunks) > 1
    assert chunks[0].metadata["file_path"] == "main.py"
    assert chunks[0].metadata["language"] == "Python"
    assert "chunk_index" in chunks[0].metadata
    assert "chunk_size" in chunks[0].metadata