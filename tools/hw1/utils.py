import re 
import math
from functools import reduce
from collections import deque


def parse_and_gcd(text):
    pattern = re.compile(r'\w+: count=\d+, positions=\[.*?\], diffs=\[(.*?)\]')
    diffs = []

    for match in pattern.finditer(text):
        diff_str = match.group(1)
        diff_list = list(map(int, diff_str.split(',')))
        diffs.extend(diff_list)

    if not diffs:
        return None

    return reduce(math.gcd, diffs)


def multiply_shifted(dict1, dict2, n):
    keys = list(dict2.keys())
    values = list(dict2.values())
    
    # 使用 deque 实现循环右移
    shifted_values = deque(values)
    shifted_values.rotate(n)
    shifted_values = list(shifted_values)
    
    shifted_dict2 = dict(zip(keys, shifted_values))
    
    return {key: dict1[key] * shifted_dict2[key] for key in dict1}



letter_probabilities = {
    'A': 0.082,
    'B': 0.015,
    'C': 0.028,
    'D': 0.043,
    'E': 0.127,
    'F': 0.022,
    'G': 0.020,
    'H': 0.061,
    'I': 0.070,
    'J': 0.002,
    'K': 0.008,
    'L': 0.040,
    'M': 0.024,
    'N': 0.067,
    'O': 0.075,
    'P': 0.019,
    'Q': 0.001,
    'R': 0.060,
    'S': 0.063,
    'T': 0.091,
    'U': 0.028,
    'V': 0.010,
    'W': 0.023,
    'X': 0.001,
    'Y': 0.020,
    'Z': 0.001
}
    