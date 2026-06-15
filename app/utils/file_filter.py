from pathlib import Path

IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "target",
    ".next",
    ".nuxt",
    "coverage",
}

IGNORED_FILES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".cs",
    ".html",
    ".css",
    ".scss",
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React JSX",
    ".tsx": "React TSX",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".cs": "C#",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".md": "Markdown",
    ".txt": "Text",
    ".json": "JSON",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".ini": "Config",
    ".cfg": "Config",
}

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

def should_ignore_directory(directory_name: str) -> bool:
    return directory_name in IGNORED_DIRECTORIES

def should_include_file(file_path: Path) -> bool:
    if file_path.name in IGNORED_FILES:
        return False
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False
    if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
        return False
    
    return True

def detect_language(file_path: Path) -> str:
    return LANGUAGE_BY_EXTENSION.get(file_path.suffix.lower(), "Unknown")
