"""
Miscellaneous methods
"""

import sys

def progress_str(n1, n2):
    msg = '    %d/%d Completed' % (n1, n2)
    return len(msg) * '\b' + msg

def print_progress_str(n1, n2, end=''):
    print(progress_str(n1, n2), end=end)
    sys.stdout.flush()