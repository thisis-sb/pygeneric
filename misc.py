"""
Miscellaneous methods
"""

import sys
from math import isnan, nan
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

def eval_formula(formula_str, attr_dict, nan_as_zero=False, round_to=2, verbose=False):
    ''' parse & evaluate formula '''
    if verbose:
        print('eval_formula: formula_str:', formula_str)
    still_there = True
    while still_there:
        x1 = formula_str.split('[')
        if len(x1) > 1:
            x2 = x1[1].split(']')
            if len(x2) > 1:
                attr_1 = x2[0]
            else:
                still_there = False
                continue
            ''' harsh: proceed only if present in attr_dict'''
            assert attr_1 in attr_dict.keys(), f'{attr_1} not in attr_dict'
            attr_val = attr_dict[attr_1] if attr_1 in list(attr_dict.keys()) else nan
            if nan_as_zero and isnan(attr_val):
                attr_val = 0
            formula_str = formula_str.replace('[%s]' % attr_1, f'{attr_val}')
        else:
            still_there = False
            continue
    if verbose:
        print('    parsed to:', formula_str, end=', ')
    assert 'system' not in formula_str, 'formula_str: %s' % formula_str

    if 'nan' in formula_str and not nan_as_zero:
        val = nan
    else:
        try:
            val = round(eval(formula_str), 2)
        except ZeroDivisionError:
            val = nan
    if verbose:
        print('result:', val)

    return val