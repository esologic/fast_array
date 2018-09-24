from multiprocessing import Process, Queue
from ctypes import c_int
from code.fast_array import buffer_extract, buffer_insert, FastArrayDataStructures
from datetime import datetime


def send_with_fast_array(lock, count_index, data_index, count_array, data_array, results):
    start = datetime.now()
    buffer_extract(lock, count_index, data_index, count_array, data_array)
    end = datetime.now()
    delta = (end-start).total_seconds()
    results.put(delta)


def send_with_queue(queue, results):
    start = datetime.now()
    queue.get()
    end = datetime.now()
    delta = (end-start).total_seconds()
    results.put(delta)


if __name__ == "__main__":

    results_queue = Queue()
    results_fa = Queue()

    for i in range(0, 2000, 100):

        send_me = list(range(0, i * i))

        print("Test with size", str(len(send_me)))

        s = FastArrayDataStructures(1, c_int, len(send_me))
        q = Queue()

        fa_process = Process(target=send_with_fast_array, args=[s.lock, s.count_index, s.data_index, s.count_array, s.data_array, results_fa])
        pipe_process = Process(target=send_with_queue, args=[q, results_queue])

        q.put(send_me)
        pipe_process.start()
        pipe_process.join()

        buffer_insert(s.lock, s.count_index, s.data_index, s.count_array, s.data_array, send_me)
        fa_process.start()
        fa_process.join()

    while (results_queue.empty() == False) and (results_fa.empty() == False):
        print("Queue", results_queue.get(), "FA", results_fa.get())
