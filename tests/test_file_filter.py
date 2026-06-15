from pathlib import Path

from app.utils.file_filter import detect_language, should_ignore_directory


def test_should_ignore_node_modules():
    assert should_ignore_directory("node_modules")


def test_should_ignore_git_directory():
    assert should_ignore_directory(".git")


def test_should_not_ignore_app_directory():
    assert not should_ignore_directory("app")


def test_detect_python_language():
    assert detect_language(Path("main.py")) == "Python"


def test_detect_javascript_language():
    assert detect_language(Path("index.js")) == "JavaScript"


def test_detect_unknown_language():
    assert detect_language(Path("binary.exe")) == "Unknown"