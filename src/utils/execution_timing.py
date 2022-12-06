from datetime import datetime as dt

from termcolor import colored


def record_execution_time(f, *args):
    start = dt.now()
    res = f(*args)
    end = dt.now()
    duration = end - start
    return res, (start, end, duration)
