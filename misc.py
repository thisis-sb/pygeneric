"""
Miscellaneous methods
"""

import sys
import pandas as pd

def progress_str(n1, n2):
    msg = '    %d/%d Completed' % (n1, n2)
    return len(msg) * '\b' + msg

def print_progress_str(n1, n2, end=''):
    print(progress_str(n1, n2), end=end)
    sys.stdout.flush()

def df2print_segrows(df, col):
    ''' Silly but works '''
    mask = df[col].ne(df[col].shift(-1))
    df1 = pd.DataFrame('', index=mask.index[mask] + .5, columns=df.columns)
    df = pd.concat([df, df1]).sort_index().reset_index(drop=True).iloc[:-1]
    return df