import unicodedata
"""Functions related to CJK characters"""

def count_cjk_chars(s):
    """Count numbers of CJK characters in a string.

    Arguments:
    s -- the string contains CJK characters
    """
    counts = 0
    for c in s:
        if unicodedata.east_asian_width(c) in 'WF':
            counts += 1
    return counts
