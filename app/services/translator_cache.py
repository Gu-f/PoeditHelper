import threading


class TranslatorCache:
    def __init__(self):
        self._lock = threading.Lock()
        self._cache = {}

    def get(self, category: str):
        with self._lock:
            return self._cache.get(category)

    def set(self, category: str, translator):
        with self._lock:
            self._cache[category] = translator

    def has(self, category: str) -> bool:
        with self._lock:
            return category in self._cache
