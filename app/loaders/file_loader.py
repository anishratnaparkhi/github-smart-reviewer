from pathlib import Path

from app.utils.file_filter import(
    detect_language,
    should_ignore_directory,
    should_include_file,
)

def count_lines(file_path: Path) -> int:
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for _ in file)  # the sum apprach is memory efficient as it does not load the entire file into memory rather iterates over the file line by line.
    except OSError:
        return 0

def scan_repository(repo_path: Path) -> dict:
    selected_files = []
    skipped_files = []
    total_files_scanned = 0

    for file_path in repo_path.rglob("*"):   # rglob is used to recursively search for files in the repository. * matches all the files and directories.
        if file_path.is_dir():
            continue

        relative_path = file_path.relative_to(repo_path)

        if any(should_ignore_directory(part) for part in relative_path.parts):
            skipped_files.append(
                {
                    "path": str(relative_path),
                    "reason": "Ignored directory",
                }
            )
            continue

        total_files_scanned += 1

        if should_include_file(file_path):
            selected_files.append(
                {
                    "path": str(relative_path),
                    "absolute_path": str(file_path),
                    "language": detect_language(file_path),
                    "extension": file_path.suffix.lower(),
                    "size_bytes": file_path.stat().st_size,
                    "line_count": count_lines(file_path),
                }
            )
        else:
            skipped_files.append({
                "path": str(relative_path),
                "reason": "Unsupported, ignored, or too large",
             }
        )
        
    languages = sorted({
        file_info["language"]
        for file_info in selected_files
        }
    )

    return {
        "repo_path": str(repo_path),
        "total_files_scanned": total_files_scanned,
        "selected_file_count": len(selected_files),
        "skipped_file_count": len(skipped_files),
        "languages": languages,
        "selected_files": selected_files,
        "skipped_files": skipped_files,
    }
