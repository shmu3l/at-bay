from datetime import datetime
from cacheout import Cache


class ScansCache:
    # cache with maxsize
    cache = Cache(maxsize=256, ttl=2000)

    def set_cache(self, uid: str, value):
        update_value = self.timestemp(value)
        self.cache.set(uid, update_value, ttl=2000)
        return update_value

    def get_cache(self, uid: str):
        if self.cache.get(uid):
            return self.cache.get(uid)

        return "NOT_FOUND"

    def update_status(self, uid, status):
        item = self.get_cache(uid)
        item.status = status
        self.set_cache(uid, item)
        return self.get_cache(uid)

    def timestemp(self, value):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        value.ttl = current_time
        return value

    def clear_all(self):
        self.cache.clear()
        return len(self.cache) == 0

    def get_all(self):
        cache_items = self.cache.items()
        return cache_items

