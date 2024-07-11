"""
financial utils
"""
''' --------------------------------------------------------------------------------------- '''

from datetime import date

def ind_fy_and_qtr(period_end):
    # YYYY-xxYY-Qx - as per IND Fiscal Year
    if period_end == 'not-found':
        return 'not-found'
    qtr_map = {'06':'Q1', '09':'Q2', '12':'Q3', '03':'Q4'}
    qtr = qtr_map[period_end[5:7]]
    if qtr == 'Q4':
        fy = '%d-%s' % (int(period_end[0:4])-1, period_end[0:4])
    else:
        fy = '%s-%d' % (period_end[0:4], int(period_end[0:4])+1)
    return '%s-%s-%s' % (fy[0:4], fy[7:], qtr)

def ind_fy(dt):
    cut_off = date(dt.year, 3, 31)
    if dt <= cut_off:
        return 'FY%d-%2d' % (dt.year-1, dt.year % 2000)
    else:
        return 'FY%d-%2d' % (dt.year, (dt.year + 1) % 2000)

def test_me():
    assert ind_fy(date(2023, 3, 30)) == 'FY2022-23'
    assert ind_fy(date(2023, 1, 1)) == 'FY2022-23'
    assert ind_fy(date(2023, 3, 31)) == 'FY2022-23'
    assert ind_fy(date(2022, 12, 31)) == 'FY2022-23'
    assert ind_fy(date(2022, 10, 3)) == 'FY2022-23'
    assert ind_fy(date(2022, 4, 1)) == 'FY2022-23'
    assert ind_fy(date(2022, 6, 17)) == 'FY2022-23'
    print('fin_utils.test_me passed\n')
    return True

''' -------------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    test_me()