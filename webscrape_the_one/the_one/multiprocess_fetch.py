import multiprocessing
from .main import main


# utility - spawn a thread to execute target for each args
def parallel_map(func, data):
    """
    Similar to the bultin function map(). But spawn a thread for each argument
    and apply `func` concurrently.

    Note: unlike map(), we cannot take an iterable argument. `data` should be an
    indexable sequence.
    """

    N = len(data)
    manager = multiprocessing.Manager()
    result = manager.list()

    processes = [multiprocessing.Process(target=call_main, args=(result, data[i],)) for i in range(N)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    return result


def call_main(retr, url):
    retr.append(main(product=url))
