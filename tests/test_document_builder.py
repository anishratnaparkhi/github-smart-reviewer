from pathlib import Path

from app.indexing.document_builder import build_document_from_scan


def test_build_document_from_scan(tmp_path):
    sample_file = tmp_path / "main.py"
    sample_file.write_text("print('hello')", encoding="utf-8")

    scan_result = {
        "selected_files": [
            {
                "path": "main.py",
                "absolute_path": str(sample_file),
                "language": "Python",
                "extension": ".py",
                "size_bytes": sample_file.stat().st_size,
                "line_count": 1,
            }
        ]
    }

    documents = build_document_from_scan(scan_result)

    assert len(documents) == 1
    assert documents[0].page_content == "print('hello')"
    assert documents[0].metadata["file_path"] == "main.py"
    assert documents[0].metadata["language"] == "Python"