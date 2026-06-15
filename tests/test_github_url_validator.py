from app.utils.github_url_validator import(
    get_repo_name,
    normalize_github_url,
    validate_github_url,
)

def test_valid_github_url():
    assert validate_github_url("https://github.com/pallets/flask")

def test_valid_github_url_with_git_suffix():
    assert validate_github_url("https://github.com/pallets/flask.git")


def test_invalid_non_github_url():
    assert not validate_github_url("https://gitlab.com/pallets/flask")

def test_invalid_missing_https():
    assert not validate_github_url("github.com/pallets/flask")


def test_normalize_github_url_removes_git_suffix():
    assert normalize_github_url("https://github.com/pallets/flask.git") == "https://github.com/pallets/flask"


def test_get_repo_name():
    assert get_repo_name("https://github.com/pallets/flask") == "flask"