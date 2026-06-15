import shutil
import time
import os
import stat
from pathlib import Path
from app.config import TEMP_REPOS_DIR, VECTOR_STORE_DIR

def remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def remove_directory(directory_path: Path) -> None:
    if directory_path.exists() and directory_path.is_dir():
        try:
            shutil.rmtree(directory_path, onexc=remove_readonly)
        except TypeError:
            # Fallback for Python < 3.12
            shutil.rmtree(directory_path, onerror=remove_readonly)

def cleanup_repo_directory(session_id: str) -> None:
    repo_path = TEMP_REPOS_DIR / session_id
    remove_directory(repo_path)

def cleanup_expired_sessions(max_age_hours: int = 24) -> None:
    now = time.time()
    max_age_seconds = max_age_hours * 3600

    # Scan and cleanup expired temp repositories
    if TEMP_REPOS_DIR.exists():
        for session_dir in TEMP_REPOS_DIR.iterdir():
            if session_dir.is_dir():
                mtime = session_dir.stat().st_mtime
                if (now - mtime) > max_age_seconds:
                    remove_directory(session_dir)

    # Scan and cleanup expired vector stores
    if VECTOR_STORE_DIR.exists():
        for session_dir in VECTOR_STORE_DIR.iterdir():
            if session_dir.is_dir():
                mtime = session_dir.stat().st_mtime
                if (now - mtime) > max_age_seconds:
                    remove_directory(session_dir)

