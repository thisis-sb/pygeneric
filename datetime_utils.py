import time

time_counters = None
def time_since_last(id, precision=0):
    global time_counters

    if time_counters is None:
        time_counters = [None, None, None, None, None]

    if time_counters[id] is None:
        time_counters[id] = time.time()
        tsl = 0.0
    else:
        t1 = time_counters[id]
        time_counters[id] = time.time()
        tsl = int(time_counters[id] - t1) if precision == 0 else \
            round(time_counters[id] - t1, precision)
    return tsl