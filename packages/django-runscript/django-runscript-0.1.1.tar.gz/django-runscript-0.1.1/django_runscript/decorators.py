import traceback
from logging import Logger
from threading import Thread
from time import sleep
from typing import Callable


def daemon(function: Callable, interval: float, logger: Logger = None) -> Callable:
    def decorator(*args, **kwargs):
        while True:
            try:
                function(*args, **kwargs)
            except Exception as exception:
                if logger is None:
                    traceback.print_exc()
                else:
                    logger.exception(exception)
            sleep(interval)

    return decorator


def parallel(function: Callable, concurrency: int, logger: Logger = None) -> Callable:
    def decorator(*args, **kwargs):
        def worker():
            try:
                function(*args, **kwargs)
            except Exception as exception:
                if logger is not None:
                    logger.exception(exception)
                raise

        threads = [Thread(target=worker) for _ in range(concurrency)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    return decorator
