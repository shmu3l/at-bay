import redis

from ingest import IngestQueue
from cyber_scan import check_url_status

NUMBER_OF_TASKS = 50


def test_bulk_scan():
    for num in range(NUMBER_OF_TASKS):
        scan_instance = queue.enqueue(check_url_status, "google.com")
        # print(scan_instance.id)
    return True


if __name__ == '__main__':
    r = redis.Redis()
    queue = IngestQueue(r, "cyber_scan")
    test_bulk_scan()
    print(f"Enqueued {queue.get_length()} scans!")
