import sys

import redis

from ingest import IngestQueue

s = input("enter scan_id> ")


def main():
    r = redis.Redis()
    queue = IngestQueue(r, "cyber_scan")
    item = queue.by_id(s)
    print(f"[{item.id}][{item.ttl}] Status is : {item.status}")


if __name__ == "__main__":
    main()