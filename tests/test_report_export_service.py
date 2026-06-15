from app.services.report_export_service import (
    build_markdown_report,
    create_report_filename,
)


def test_create_report_filename():
    assert create_report_filename("my repo") == "my-repo-review-report.md"


def test_build_markdown_report_contains_main_sections():
    report = build_markdown_report(
        repo_info={
            "repo_name": "demo",
            "repo_url": "https://github.com/user/demo",
            "session_id": "abc123",
        },
        scan_result={
            "total_files_scanned": 10,
            "selected_file_count": 5,
            "skipped_file_count": 5,
            "languages": ["Python"],
        },
        indexing_result={
            "document_count": 5,
            "chunk_count": 20,
        },
        review_report={
            "summary": "summary",
            "architecture": "architecture",
            "code_quality": "quality",
            "security": "security",
            "testing": "testing",
            "readme": "readme",
        },
        internship_report={
            "score": "score",
            "resume": "resume",
            "interview_explanations": "explanations",
            "interview_qa": "qa",
        },
    )

    assert "# Smart GitHub Project Reviewer Report" in report
    assert "https://github.com/user/demo" in report
    assert "summary" in report
    assert "resume" in report
    assert "score" in report