# CJKStr -- A Simple Package for Processing CJK string

In Python, the string formatting function will treat a CJK characters as wide as a english letter.This make the result weired. For example:

```Python
print("1234567890" * 4) 
a = "測試"
w = 10
print(f"{a:{w}s}|")
```

produce output as this:

```python
1234567890123456789012345678901234567890
測試        |
```

The width is setting to 10 in the formatting string. Since the 2 Chinese characters occupies 2 more spaces, the bar is printed in position 13.

To avoid this problem, we need to know how many CJK Chinese characters in the string and resuce the width accorantly.

This package has only one funcion:

```python
count_cjk_chars(s) # return number of chinese characters in string s
```

### example
```python
import cjkstr

print("1234567890" * 4) 
a = "測試"
w = 10
print(f"{a:{w}s}|")
w = 10 - cjkstr.count_cjk_chars(a)
print(f"{a:{w}s}|")
```

ouput:

```python
1234567890123456789012345678901234567890
測試        |
測試      |
```

