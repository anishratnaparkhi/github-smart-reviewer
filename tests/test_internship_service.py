from app.services.internship_service import combine_core_report


def test_combine_core_report_contains_all_sections():
    review_report = {
        "summary": "summary text",
        "architecture": "architecture text",
        "code_quality": "quality text",
        "security": "security text",
        "testing": "testing text",
        "readme": "readme text",
    }

    result = combine_core_report(review_report)

    assert "summary text" in result
    assert "architecture text" in result
    assert "quality text" in result
    assert "security text" in result
    assert "testing text" in result
    assert "readme text" in result