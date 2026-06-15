import pytest

from app.indexing.embedding import EmbeddingConfigError

def test_embedding_config_error_exists():
    error = EmbeddingConfigError("test")
    assert str(error) == "test"


