"""
Miscellaneous methods
"""
''' ------------------------------------------------------------------------------------------ '''

import sys
import math
import re
import pandas as pd

def progress_str(n1, n2):
    msg = '    %d/%d Completed' % (n1, n2)
    return len(msg) * '\b' + msg

def print_progress_str(n1, n2, end=''):
    print(progress_str(n1, n2), end=end)
    sys.stdout.flush()

def method(qual=None):
    from traceback import extract_stack
    m = str(extract_stack()[-2]).split()[-1].split('>')[0]
    return '%s.%s' % (qual, m) if qual is not None else m

def is_number(num_str):
    try:
        float(num_str)
    except ValueError:
        return False
    return True

def segregate_rows(df, col):
    ''' Silly but works '''
    mask = df[col].ne(df[col].shift(-1))
    df1 = pd.DataFrame('', index=mask.index[mask] + .5, columns=df.columns)
    df = pd.concat([df, df1]).sort_index().reset_index(drop=True).iloc[:-1]
    return df

def eval_formula(formula_str, metrics_dict, nan_as_zero=False, round_to=2, verbose=False):
    if verbose:
        print('eval_formula: formula_str:', formula_str)

    var_list = re.findall(r'\[.*?\]', formula_str)
    for var in var_list:
        val = metrics_dict[var[1:-1]] if var[1:-1] in list(metrics_dict.keys()) else math.nan
        if nan_as_zero and pd.isnull(val):
            val = 0
        formula_str = formula_str.replace(var, str(val))
    if verbose:
        print('  parsed to:', formula_str, end=', ')

    assert 'system' not in formula_str, 'formula_str: %s' % formula_str
    assert 'os' not in formula_str, 'formula_str: %s' % formula_str

    if not nan_as_zero and ('nan' in formula_str or 'NaN' in formula_str):
        formula_val = math.nan
    else:
        try:
            formula_val = round(eval(formula_str), round_to)
        except ZeroDivisionError:
            formula_val = math.nan

    if verbose:
        print('result:', formula_val)

    return formula_val

def dict_diff(d1, d2):
    ''' rudimentary; only 1 level right now '''
    key_set_1 = [k for k in d1.keys() if k in d2.keys()]
    key_set_2 = [k for k in d1.keys() if k not in d2.keys()]
    key_set_3 = [k for k in d2.keys() if k not in d1.keys()]
    diffs = {}
    for k in key_set_1:
        if d1[k] != d2[k]:
            if not (pd.isnull(d1[k]) and pd.isnull(d2[k])):
                diffs[k] = {'d1': d1[k], 'd2': d2[k]}
    for k in key_set_2:
        diffs[k] = {'d1': d1[k], 'd2': None}
    for k in key_set_3:
        diffs[k] = {'d1': None, 'd2': d2[k]}
    return diffs

''' -------------------------------------------------------------------------------------------- '''
def test_me():
    d1 = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
    d2 = {1: 'a', 4: 'd', 3: 'c', 5: 'e', 2: 'b'}
    assert dict_diff(d1, d2) == {}, dict_diff(d1, d2)

    d2[4] = 'dd'
    assert dict_diff(d1, d2) == {4: {'d1': 'd', 'd2': 'dd'}}, dict_diff(d1, d2)

    d1[5] = 'ee'
    assert dict_diff(d1, d2) == {4: {'d1': 'd', 'd2': 'dd'},
                                 5: {'d1': 'ee', 'd2': 'e'}}, dict_diff(d1, d2)

    d1.pop(3)
    d2.pop(1)
    assert dict_diff(d1, d2) == {4: {'d1': 'd', 'd2': 'dd'},
                                 5: {'d1': 'ee', 'd2': 'e'},
                                 1: {'d1': 'a', 'd2': None},
                                 3: {'d1': None, 'd2': 'c'}
                                 }, dict_diff(d1, d2)

    d1 = {1: 'a', 2: float('nan'), 3: 'c', 4: 'd', 5: 'e'}
    d2 = {1: 'a', 4: 'd', 3: 'c', 5: 'e', 2: 'b'}
    x = dict_diff(d1, d2)
    assert pd.isnull(x[2]['d1']) and x[2]['d2'] == 'b'
    x[2]['d1'] = None
    assert x == {2: {'d1': None, 'd2': 'b'}}, x

    d2[2] = float('nan')
    assert dict_diff(d1, d2) == {}, dict_diff(d1, d2)

    return True

''' -------------------------------------------------------------------------------------------- '''
if __name__ == '__main__':
    test_me()
    print('All OK')