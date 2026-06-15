import re

GITHUB_REPO_URL_PATTERN = re.compile(
    r"^https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)

def validate_github_url(repo_url: str) -> bool:
    if not repo_url:
        return False
    return bool(GITHUB_REPO_URL_PATTERN.match(repo_url.strip()))

def normalize_github_url(repo_url:str) -> str:
    cleaned_url = repo_url.strip()

    if cleaned_url.endswith("/"):
        cleaned_url = cleaned_url[:-1]
    
    if cleaned_url.endswith(".git"):
        cleaned_url = cleaned_url[:-4]

    return cleaned_url

def get_repo_name(repo_url: str) -> str:
    normalized_url = normalize_github_url(repo_url)
    return normalized_url.split("/")[-1]

