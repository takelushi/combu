"""Simple."""

import combu


def _f(v1, v2):
    return v1 + v2


params = {'v1': ['a', 'b'], 'v2': ['A', 'B']}
for res, param in combu.execute(_f, params):
    print(res, param)

# Result
"""
aA {'v1': 'a', 'v2': 'A'}
aB {'v1': 'a', 'v2': 'B'}
bA {'v1': 'b', 'v2': 'A'}
bB {'v1': 'b', 'v2': 'B'}
"""
