"""Use Combu class."""

import combu


def _f(v1, v2):
    return v1 + v2


comb = combu.Combu(_f)

params = {'v1': ['a', 'b'], 'v2': ['A', 'B']}
for res, param in comb.execute(params):
    print(res, param)

# Result
"""
aA {'v1': 'a', 'v2': 'A'}
aB {'v1': 'a', 'v2': 'B'}
bA {'v1': 'b', 'v2': 'A'}
bB {'v1': 'b', 'v2': 'B'}
"""
