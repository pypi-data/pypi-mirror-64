import unicodedata

def count_cjk_chars(s):
    counts = 0
    for c in s:
        if unicodedata.east_asian_width(c) in 'WF':
            counts += 1
    return counts
