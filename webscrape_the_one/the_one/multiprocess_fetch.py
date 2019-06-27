import multiprocessing
from .main import main


def parallel_map(func, data):

    N = len(data)
    manager = multiprocessing.Manager()
    result = manager.list()

    processes = [multiprocessing.Process(target=func, args=(result, data[i],)) for i in range(N)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    return result


def call_main(result, url):
    result.append(main(product=url))
