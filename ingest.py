import json
import pickle
import uuid
from datetime import datetime
from tinydb import TinyDB, where

# manage scans with Redis queue, we have the length of the q, enqueues and dequeues ops.
# Scan class manage the scan tasks instances (also create the uid - scan_id)
# Redis comments - https://redis.io/commands


db = TinyDB('./data/scans_db.json')


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

    def enqueue(self, scan_task):
        db.update({"status": "RUNNING"}, where('id') == scan_task.id)
        # serialized pickle way without saving file just for radis enq-deq
        serialized_task = pickle.dumps(scan_task, protocol=pickle.HIGHEST_PROTOCOL)
        self.conn.lpush(self.name, serialized_task)
        return scan_task.id

    def dequeue(self):
        # pop from queue & serialized
        _, serialized_task = self.conn.brpop(self.name)
        task = pickle.loads(serialized_task)
        updated_status_from_task = task.process_scan()
        now = datetime.now()
        ttl = now.strftime("%H:%M:%S")
        db.update({"status": updated_status_from_task, "ttl": ttl}, where('id') == task.id)
        return task


class Scan(object):

    def __init__(self, func, *args, status=None, ttl=None):
        self.id = str(uuid.uuid4())[:8]
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
        res = self.func(*self.args)
        return res

    def _to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
