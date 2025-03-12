import time
from datetime import date, datetime, timedelta

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

def remove_all_timers():
    _timers_dict.clear()

def get_month_end_dates(year):
    dates = [(datetime(year, m, 1) - timedelta(days=1)).strftime('%Y-%m-%d') for m in range(2,13)]
    dates.append((datetime(year+1, 1, 1) - timedelta(days=1)).strftime('%Y-%m-%d'))
    return sorted(dates)

def get_period_ends(**kwargs):
    pe = kwargs['pe'] if 'pe' in kwargs.keys() else None
    fp = kwargs['fp'] if 'fp' in kwargs.keys() else None
    lp = kwargs['lp'] if 'lp' in kwargs.keys() else None
    np = kwargs['np'] if 'np' in kwargs.keys() else None
    verbose = kwargs['verbose'] if 'verbose' in kwargs.keys() else False
    if verbose:
        print('\nget_period_ends: kwargs:', kwargs, end=', ')
    if pe is not None:
        period_ends = pe
    else:
        period_ends = [[f'{y}-03-31', f'{y}-06-30', f'{y}-09-30', f'{y}-12-31']
                       for y in range(2018, date.today().year+1)]
        period_ends = [p for p1 in period_ends for p in p1 if p <= date.today().strftime('%Y-%m-%d')]
        if lp is not None:
            period_ends = [p for p in period_ends if p <= lp]
        if fp is not None:
            period_ends = [p for p in period_ends if p >= fp]
        if np is not None:
            period_ends = period_ends[-np:]
    if verbose:
        print('period_ends: %s\n' % period_ends)
    return period_ends

def test_me(verbose=False):
    ''' Testing get_period_ends '''
    assert get_period_ends(pe='2024-03-31') == '2024-03-31'
    assert get_period_ends(np=5, lp='2024-03-31') ==\
           ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31']
    assert get_period_ends(np=5, fp='2018-01-01', lp='2024-03-31') == \
           ['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31']
    assert get_period_ends(np=3, fp='2018-01-01', lp='2023-06-30') == \
           ['2022-12-31', '2023-03-31', '2023-06-30']
    period_ends = get_period_ends(np=5)
    assert int(period_ends[4][0:4]) == (int(period_ends[0][0:4]) + 1)

    ''' Testing elapsed_time '''
    elapsed_time('pygeneric.datetime_utils.test_me.0')
    elapsed_time('pygeneric.datetime_utils.test_me.grand_total')
    time.sleep(2)
    t = elapsed_time('pygeneric.datetime_utils.test_me.0')
    assert 2.0 <= t <= 2.1, "should be approx. 2"

    elapsed_time(['pygeneric.datetime_utils.test_me.0',
                  'pygeneric.datetime_utils.test_me.1',
                  'pygeneric.datetime_utils.test_me.2'])
    time.sleep(3)
    t = elapsed_time(['pygeneric.datetime_utils.test_me.0', 'pygeneric.datetime_utils.test_me.2'])
    assert type(t) == list
    assert 3.0 <= t[0] < 3.1
    assert 3.0 <= t[1] < 3.1

    time.sleep(1)
    t = elapsed_time('pygeneric.datetime_utils.test_me.1')
    assert 4.0 <= t < 4.1

    time.sleep(2)
    elapsed_time(['pygeneric.datetime_utils.test_me.3', 'abc', 'pygeneric.datetime_utils.test_me.0'])
    time.sleep(1)
    t = elapsed_time(['abc', 'pygeneric.datetime_utils.test_me.1'])
    assert len(t) == 2
    assert 1.0 <= t[0] <= 1.1
    assert 3.0 <= t[1] <= 3.1

    t = elapsed_time(['pygeneric.datetime_utils.test_me.grand_total',
                      'pygeneric.datetime_utils.test_me.0',
                      'pygeneric.datetime_utils.test_me.1',
                      'pygeneric.datetime_utils.test_me.2'])
    assert len(t) == 4
    assert 9.0 <= t[0] <= 9.1
    assert 1.0 <= t[1] <= 1.1
    assert 0.0 <= t[2] <= 0.1
    assert 4.0 <= t[3] <= 4.1

    assert len(_timers_dict.keys()) >= 5
    remove_all_timers()
    assert len(_timers_dict.keys()) == 0

    assert get_month_end_dates(2022) == ['2022-01-31', '2022-02-28', '2022-03-31', '2022-04-30',
                                         '2022-05-31', '2022-06-30', '2022-07-31', '2022-08-31',
                                         '2022-09-30', '2022-10-31', '2022-11-30', '2022-12-31']
    assert get_month_end_dates(2023) == ['2023-01-31', '2023-02-28', '2023-03-31', '2023-04-30',
                                         '2023-05-31', '2023-06-30', '2023-07-31', '2023-08-31',
                                         '2023-09-30', '2023-10-31', '2023-11-30', '2023-12-31']
    assert get_month_end_dates(2024) == ['2024-01-31', '2024-02-29', '2024-03-31', '2024-04-30',
                                         '2024-05-31', '2024-06-30', '2024-07-31', '2024-08-31',
                                         '2024-09-30', '2024-10-31', '2024-11-30', '2024-12-31']

    return True

''' --------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    test_me()
    print('All tests passed!')