"""
financial utils
"""
''' --------------------------------------------------------------------------------------- '''

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