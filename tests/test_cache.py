from pathlib import Path

from adapter.utils.response_cache import EmbeddingResponseCache, build_cache_key


def test_build_cache_key_stable() -> None:
    key1 = build_cache_key("m", ["a", "b"], True, 384, "retrieval")
    key2 = build_cache_key("m", ["a", "b"], True, 384, "retrieval")
    assert key1 == key2


def test_embedding_response_cache_persistence(tmp_path: Path) -> None:
    db_path = tmp_path / "cache.sqlite3"
    cache = EmbeddingResponseCache(str(db_path), max_entries=10)
    key = build_cache_key("m", ["hello"], True, None, None)
    value = [[0.1, 0.2, 0.3]]

    cache.set(key, value)

    cache2 = EmbeddingResponseCache(str(db_path), max_entries=10)
    loaded = cache2.get(key)
    assert loaded == value
