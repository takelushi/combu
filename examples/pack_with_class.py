"""Pack combination."""

import combu
from combu import Pack


def _f(v1, v2):
    return v1 + v2


params = {
    Pack('v1', 'v2'): [
        {
            'v1': ['a', 'b'],
            'v2': ['A', 'B'],
        },
        {
            'v1': ['x', 'y'],
            'v2': ['X', 'Y'],
        },
    ],
}
for res, param in combu.execute(_f, params):
    print(res, param)

# Result
"""
aA {'v1': 'a', 'v2': 'A'}
aB {'v1': 'a', 'v2': 'B'}
bA {'v1': 'b', 'v2': 'A'}
bB {'v1': 'b', 'v2': 'B'}
xX {'v1': 'x', 'v2': 'X'}
xY {'v1': 'x', 'v2': 'Y'}
yX {'v1': 'y', 'v2': 'X'}
yY {'v1': 'y', 'v2': 'Y'}
"""
