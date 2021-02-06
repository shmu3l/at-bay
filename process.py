import multiprocessing
import time
from worker import worker

PROCESSES = 4


def run():
    processes = []
    print(f"Running with {PROCESSES} processes!")
    while True:
        # time.sleep(5)
        for w in range(PROCESSES):
            p = multiprocessing.Process(target=worker)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()


if __name__ == '__main__':
    run()
