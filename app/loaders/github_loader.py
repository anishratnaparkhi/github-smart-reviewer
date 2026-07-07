from pathlib import Path
from uuid import uuid4

from git import Repo, GitCommandError

from app.config import TEMP_REPOS_DIR
from app.utils.cleanup import remove_directory
from app.utils.github_url_validator import(
    get_repo_name,
    normalize_github_url,
    validate_github_url,
)

class GitHubLoaderError(Exception):
    pass

def clone_github_repo(repo_url:str) -> dict:
    if not validate_github_url(repo_url):
        raise GitHubLoaderError("Please enter a valid public Github repository URL.")
    
    normalized_url = normalize_github_url(repo_url)
    repo_name = get_repo_name(normalized_url)
    session_id = str(uuid4())

    target_dir = TEMP_REPOS_DIR / session_id / repo_name
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    # setting the parameter parents = True allows to make intermediate directories in the path if they do not exist. exist_ok = True allows to avoid raising an error if the directory already exists.

    try:
        Repo.clone_from(normalized_url, target_dir, depth=1)

    # depth = 1 allows us to create a shallow copy of only the latest commit of the repository, saving disk space.
    
    except GitCommandError as exc:
        remove_directory(target_dir.parent)
        raise GitHubLoaderError("Could not clone this repository. Make sure it is public and the URL is correct.") from exc
    
    return {
        "repo_url": normalized_url,
        "repo_name": repo_name,
        "session_id": session_id,
        "local_path": target_dir,
    }

