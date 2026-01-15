import math
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from time import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('artifacts/task2.log'),
        logging.StreamHandler(sys.stderr)
    ]
)


def integrate_chunk(f, a, start, end, step):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_class):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    
    with executor_class(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != n_jobs - 1 else n_iter
            futures.append(executor.submit(integrate_chunk, f, a, start, end, step))
        
        return sum(future.result() for future in futures)


if __name__ == "__main__":
    f = math.cos
    a = 0
    b = math.pi / 2
    cpu_count = os.cpu_count() or 1
    n_jobs_list = range(1, cpu_count * 2 + 1)

    for n_jobs in n_jobs_list:
        start = time()
        result_thread = integrate(f, a, b, n_jobs=n_jobs, executor_class=ThreadPoolExecutor)
        thread_time = time() - start

        start = time()
        result_process = integrate(f, a, b, n_jobs=n_jobs, executor_class=ProcessPoolExecutor)
        process_time = time() - start

        assert math.isclose(result_thread, result_process, rel_tol=1e-5)
        print(f'n_jobs: {n_jobs}',
              f'ThreadPoolExecutor time: {thread_time:.5f}',
              f'ProcessPoolExecutor time: {process_time:.5f}',
              sep='\t')
