import time
import logging
import functools

logger = logging.getLogger(__name__)

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info("Выполнение функции %s заняло %.4f секунд", func.__name__, elapsed)
    return wrapper

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Функция %s с аргументами %s и %s", func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return wrapper