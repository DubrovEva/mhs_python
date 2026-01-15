import time
import threading
import multiprocessing

from pathlib import Path


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def measure_time_sync(n, repetitions):
    start = time.time()
    for _ in range(repetitions):
        fibonacci(n)
    return time.time() - start


def measure_time_threading(n, repetitions):
    start = time.time()
    threads = [threading.Thread(target=fibonacci, args=(n,)) for _ in range(repetitions)]
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    return time.time() - start


def measure_time_multiprocessing(n, repetitions):
    start = time.time()
    processes = [multiprocessing.Process(target=fibonacci, args=(n,)) for _ in range(repetitions)]
    
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    
    return time.time() - start


if __name__ == "__main__":
    n = 30
    repetitions = 10

    sync_time = measure_time_sync(n, repetitions)
    threading_time = measure_time_threading(n, repetitions)
    multiprocessing_time = measure_time_multiprocessing(n, repetitions)

    with open('artifacts/task1.txt', 'w') as f:
        print(f"Synchronous execution time: {sync_time} seconds", file=f)
        print(f"Threading execution time: {threading_time} seconds", file=f)
        print(f"Multiprocessing execution time: {multiprocessing_time} seconds", file=f)
