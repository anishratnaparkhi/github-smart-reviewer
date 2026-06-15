from pathlib import Path

from langchain_core.documents import Document

def read_file_content(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding='utf-8', errors='ignore')

    except OSError:
        return ""
    
def build_document_from_scan(scan_result: dict) -> list[Document]:
    documents = []
    for file_info in scan_result["selected_files"]:
        absolute_path = Path(file_info["absolute_path"])
        content = read_file_content(absolute_path)

        if not content.strip():
            continue

        document = Document(
            page_content = content,
            metadata = {
                "file_path": file_info["path"],
                "absolute_path": file_info["absolute_path"],
                "language": file_info["language"],
                "extension": file_info["extension"],
                "size_bytes": file_info["size_bytes"],
                "line_count": file_info["line_count"],
            },
        )

        documents.append(document)

    return documents
