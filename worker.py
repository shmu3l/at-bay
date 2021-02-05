import redis
from ingest import IngestQueue


def worker():
    r = redis.Redis()
    queue = IngestQueue(r, "cyber_scan")
    if queue.get_length() > 0:
        queue.dequeue()
    else:
        print("*********** [No scans in the queue] ***********")


if __name__ == "__main__":
    worker()
