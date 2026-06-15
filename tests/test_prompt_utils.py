from langchain_core.documents import Document

from app.chains.prompt_utils import format_documents_for_prompt


def test_format_documents_for_prompt_includes_metadata_and_content():
    documents = [
        Document(
            page_content="print('hello')",
            metadata={
                "file_path": "main.py",
                "language": "Python",
            },
        )
    ]

    result = format_documents_for_prompt(documents)

    assert "CHUNK 1" in result
    assert "File: main.py" in result
    assert "Language: Python" in result
    assert "print('hello')" in result