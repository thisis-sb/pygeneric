import time
from datetime import date, datetime

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

def last_n_pe_dates(n, last_period=None):
    end_date_str = date.today().strftime('%Y-%m-%d') if last_period is None else last_period
    pe_dates = []
    for yr in range(2018, datetime.strptime(end_date_str, '%Y-%m-%d').year + 1):
        for dt in ['%d-03-31' % yr, '%d-06-30' % yr, '%d-09-30' % yr, '%d-12-31' % yr]:
            if dt <= end_date_str:
                pe_dates.append(dt)
    return pe_dates[-n:]

def get_period_ends(**kwargs):
    pe = kwargs['pe'] if 'pe' in kwargs.keys() else None
    lp = kwargs['lp'] if 'lp' in kwargs.keys() else None
    np = kwargs['np'] if 'np' in kwargs.keys() else None
    verbose = kwargs['verbose'] if 'verbose' in kwargs.keys() else False
    if verbose:
        print('\nget_period_ends: kwargs:', kwargs, end=', ')
    if pe is not None:
        period_ends = pe
    else:
        last_period = lp if lp is not None else date.today().strftime('%Y-%m-%d')
        period_ends = last_n_pe_dates(np, last_period=last_period)
    if verbose:
        print('period_ends: %s\n' % period_ends)
    return period_ends

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