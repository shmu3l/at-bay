import json
import pickle


# manage Redis queue, we have the length of the q, enqueues and dequeues ops.
# Scan class manage the scan tasks instances (also create the uid - scan_id)
# Redis comments - https://redis.io/commands
from cache_store.load_cache import CacheInit


class IngestQueue(object):

    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    def get_length(self):
        return self.conn.llen(self.name)

    def by_id(self, id):
        all_scan_tasks = self.conn.lrange(self.name, 0, -1)
        res = list()
        for serialized_task in all_scan_tasks:
            task = pickle.loads(serialized_task)
            if int(task.id) == int(id):
                res.append(task)
        return res[0]

    def enqueue(self, func, *args):
        scan_task = Scan(func, *args, status="ACCEPTED")
        cache_k = CacheInit.cache.set_cache(scan_task.id, scan_task)
        print(cache_k)
        serialized_task = pickle.dumps(scan_task, protocol=pickle.HIGHEST_PROTOCOL)
        self.conn.lpush(self.name, serialized_task)
        return scan_task

    def dequeue(self):
        _, serialized_task = self.conn.brpop(self.name)
        task = pickle.loads(serialized_task)
        task.update_status("RUNNING")
        task.process_scan()
        return task


class Scan(object):
    scanID = 0
    easyGenID = (x for x in range(1, 100))

    def __init__(self, func, *args, status=None, ttl=None):
        # self.id = uuid.uuid4().hex
        Scan.scanID += 1
        self.id = Scan.easyGenID.__next__()
        self.func = func
        self.args = args
        self.status = status
        self.ttl = ttl

    def update_status(self, status):
        self.status = status
        return self

    def update_ttl(self, ttl):
        self.ttl = ttl
        return self

    def process_scan(self):
        self.func(*self.args)

    def _to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
