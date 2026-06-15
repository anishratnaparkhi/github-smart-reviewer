import pytest

from app.indexing.vector_store import build_vector_store

def test_build_vector_store_rejects_empty_chunks():
    with pytest.raises(ValueError):
        build_vector_store([])

