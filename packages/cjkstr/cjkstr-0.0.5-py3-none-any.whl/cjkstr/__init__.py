import unicodedata
"""Functions related to CJK characters"""

def count_cjk_chars(s):
    """Count numbers of CJK characters in a string.

    Arg:
        s (str): The string contains CJK characters.

    Returns:
        int: The number of CJK characters.
    """
    if not (type(s) is str):
        raise TypeError("count_cjk_str only accept string.")
    counts = 0
    for c in s:
        if unicodedata.east_asian_width(c) in 'WF':
            counts += 1
    return counts

