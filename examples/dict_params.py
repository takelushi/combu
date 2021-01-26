"""dict Parameters."""

import combu


def _f(v, d):
    return '{} - {}'.format(v, d['a'] + d['b'])


d = {
    'a': [1, 10],
    'b': [1, 2, 3],
}
params = {
    'v': ['a', 'b'],
    'd': combu.create_values(d),
}

for res, param in combu.execute(_f, params):
    print(res, param)

# Result
"""
a - 2 {'v': 'a', 'd': {'a': 1, 'b': 1}}
a - 3 {'v': 'a', 'd': {'a': 1, 'b': 2}}
a - 4 {'v': 'a', 'd': {'a': 1, 'b': 3}}
a - 11 {'v': 'a', 'd': {'a': 10, 'b': 1}}
a - 12 {'v': 'a', 'd': {'a': 10, 'b': 2}}
a - 13 {'v': 'a', 'd': {'a': 10, 'b': 3}}
b - 2 {'v': 'b', 'd': {'a': 1, 'b': 1}}
b - 3 {'v': 'b', 'd': {'a': 1, 'b': 2}}
b - 4 {'v': 'b', 'd': {'a': 1, 'b': 3}}
b - 11 {'v': 'b', 'd': {'a': 10, 'b': 1}}
b - 12 {'v': 'b', 'd': {'a': 10, 'b': 2}}
b - 13 {'v': 'b', 'd': {'a': 10, 'b': 3}}
"""
