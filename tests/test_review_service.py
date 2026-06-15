from app.services.review_service import generate_core_review_report


class FakeRetriever:
    def invoke(self, query):
        return []


def test_generate_core_review_report_shape(monkeypatch):
    monkeypatch.setattr(
        "app.services.review_service.generate_repository_summary",
        lambda retriever: "summary",
    )
    monkeypatch.setattr(
        "app.services.review_service.generate_architecture_review",
        lambda retriever: "architecture",
    )
    monkeypatch.setattr(
        "app.services.review_service.generate_code_quality_review",
        lambda retriever: "quality",
    )
    monkeypatch.setattr(
        "app.services.review_service.generate_security_review",
        lambda retriever: "security",
    )
    monkeypatch.setattr(
        "app.services.review_service.generate_testing_review",
        lambda retriever: "testing",
    )
    monkeypatch.setattr(
        "app.services.review_service.generate_readme_review",
        lambda retriever: "readme",
    )

    report = generate_core_review_report(FakeRetriever())

    assert report["summary"] == "summary"
    assert report["architecture"] == "architecture"
    assert report["code_quality"] == "quality"
    assert report["security"] == "security"
    assert report["testing"] == "testing"
    assert report["readme"] == "readme"