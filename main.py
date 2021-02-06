import redis
from ingest import IngestQueue, Scan
from cyber_scan import check_url_status
from tinydb import TinyDB, where

NUMBER_OF_TASKS = 100


def test_bulk_scan():
    for num in range(NUMBER_OF_TASKS):
        scan_task = Scan(check_url_status, "google.com", status="ACCEPTED")
        db.insert({"id": scan_task.id,
                   "ttl": scan_task.ttl,
                   "status": scan_task.status})
        scan_instance = queue.enqueue(scan_task)
        print('[scan_id]', scan_instance)
    return scan_instance


if __name__ == '__main__':
    r = redis.Redis()
    queue = IngestQueue(r, "cyber_scan")
    db = TinyDB('./data/scans_db.json')
    test_bulk_scan()
    print(f"Total Scan Queue :  {queue.get_length()}")

