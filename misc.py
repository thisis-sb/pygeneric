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

    # I think this is not needed --> remove later, once sure
    # if not nan_as_zero and ('nan' in formula_str or 'NaN' in formula_str):
    #    formula_val = math.nan
    # else:

    try:
        formula_val = round(eval(formula_str), round_to)
    except ZeroDivisionError:
        formula_val = math.nan

    if verbose:
        print('result:', formula_val)

    return formula_val