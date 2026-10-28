from .lru_cache import SimpleLRUCache

def test_cache_hits_and_misses():
    cache = SimpleLRUCache(capacity=3)
    assert cache.get("k1") is None
    cache.put("k1", "v1")
    assert cache.get("k1") == "v1"
    
    st = cache.stats()
    assert st["hits"] == 1
    assert st["misses"] == 1
    assert st["size"] == 1

def test_lru_eviction_order():
    cache = SimpleLRUCache(capacity=3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    # Access "a", making "b" the least recently used
    assert cache.get("a") == 1
    
    # Adding "d" should evict "b"
    cache.put("d", 4)
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3
    assert cache.get("d") == 4
    
    st = cache.stats()
    assert st["evictions"] == 1
    assert st["size"] == 3

def test_manual_evict():
    cache = SimpleLRUCache(capacity=5)
    cache.put("x", 100)
    assert cache.evict("x") is True
    assert cache.evict("x") is False
    assert cache.get("x") is None
