from datetime import datetime as dt


def record_execution_time(f, *args):
    start = dt.now()
    res = f(*args)
    end = dt.now()
    duration = (end - start)
    print(f"\nExecution time: {duration}")
    return res, duration
