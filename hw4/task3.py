import multiprocessing
import queue
import time
import codecs
import logging
import sys
from pathlib import Path

STOP_SIGNAL = "STOP"

Path('artifacts').mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(processName)s | %(message)s',
    handlers=[
        logging.FileHandler('artifacts/task3.log'),
        logging.StreamHandler(sys.stderr)
    ]
)


def process_a(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if message == STOP_SIGNAL:
            output_queue.put(STOP_SIGNAL)
            break
        lower_message = message.lower()
        logging.info(f"Lowercased: {lower_message!r}")
        output_queue.put(lower_message)
        time.sleep(5)


def process_b(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if message == STOP_SIGNAL:
            output_queue.put(STOP_SIGNAL)
            break
        rot13_message = codecs.encode(message, 'rot_13')
        logging.info(f"Encrypted: {rot13_message!r}")
        output_queue.put(rot13_message)


if __name__ == "__main__":
    queue_a = multiprocessing.Queue(maxsize=100)
    queue_b = multiprocessing.Queue(maxsize=100)
    queue_c = multiprocessing.Queue(maxsize=100)

    process_a_instance = multiprocessing.Process(target=process_a, args=(queue_a, queue_b), name='Process A')
    process_b_instance = multiprocessing.Process(target=process_b, args=(queue_b, queue_c), name='Process B')

    process_a_instance.start()
    process_b_instance.start()

    try:
        while True:
            message = input("Enter a message (or 'STOP' to end): ")
            logging.info(f"Sending: {message!r}")
            queue_a.put(message)
            
            if message == STOP_SIGNAL:
                break

            try:
                while True:
                    response = queue_c.get(block=False)
                    if response == STOP_SIGNAL:
                        break
                    logging.info(f"Received: {response!r}")
            except queue.Empty:
                logging.info("No new messages yet")
    except KeyboardInterrupt:
        logging.info("Interrupted")
    finally:
        if not queue_a.empty() or message != STOP_SIGNAL:
            queue_a.put(STOP_SIGNAL)
        process_a_instance.join()
        process_b_instance.join()
