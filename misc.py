def progress_str(n1, n2):
    msg = '    %d/%d Completed' % (n1, n2)
    return len(msg) * '\b' + msg