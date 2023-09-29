import time

_timers_dict = {}
def _time_since_last(id, precision=0):
    global _timers_dict
    if id not in _timers_dict.keys():
        _timers_dict[id] = time.time()
        et = 0.0
    else:
        t1 = _timers_dict[id]
        _timers_dict[id] = time.time()
        et = _timers_dict[id] - t1
    return int(et) if precision == 0 else round(et, precision)

def elapsed_time(id, precision=2):
    if type(id) == list:
        return [_time_since_last(i, precision) for i in id]
    else:
        return _time_since_last(id, precision)

def remove_timers(id):
    [_timers_dict.pop(x) for x in id] if type(id) == list else _timers_dict.pop(id)

''' --------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    elapsed_time(0)
    elapsed_time('grand_total')
    time.sleep(2)
    print('should be approx. 2:', elapsed_time(0))
    elapsed_time([0, 1, 2])
    time.sleep(3)
    print('should be approx. [3, 3]:', elapsed_time([0, 2]))
    time.sleep(1)
    print('should be approx. 4:', elapsed_time(1))

    elapsed_time([3, 'abc', 0])
    time.sleep(1)
    print('should be approx. [1, 1]:', elapsed_time(['abc', 0]))
    time.sleep(1)
    print('should be approx. [2]:', elapsed_time(3))
    time.sleep(1)
    print('should be approx. [9, 2, 1, 2]:', elapsed_time(['grand_total', 0, 3, 'abc']))