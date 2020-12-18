"""Pack tuple."""

import combu


def _f(v1, v2, v3):
    return v1 + v2 + v3


# Use tuple.
params = {
    'v1': ['a', 'b'],
    ('v2', 'v3'): [
        ('A', 'X'),
        ('B', 'Y'),
    ],
}
for res, param in combu.execute(_f, params):
    print(res, param)

# Result
"""
aAX {'v1': 'a', 'v2': 'A', 'v3': 'X'}
aBY {'v1': 'a', 'v2': 'B', 'v3': 'Y'}
bAX {'v1': 'b', 'v2': 'A', 'v3': 'X'}
bBY {'v1': 'b', 'v2': 'B', 'v3': 'Y'}
"""
