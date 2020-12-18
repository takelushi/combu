"""Hook."""

from combu import Combu


def _f(v1, v2):
    print(f'Execute {v1},{v2}')


def _before_v1(v1, v2):
    print(f'Before v1 {v1},{v2}')


def _after_v1(v1, v2):
    print(f'After v1 {v1},{v2}')


def _before_each_v1(v1, v2):
    print(f'Before each v1 {v1},{v2}')


def _after_each_v1(v1, v2):
    print(f'After each v1 {v1},{v2}')


comb = Combu(_f)
comb.set_before('v1', _before_v1)
comb.set_after('v1', _after_v1)
comb.set_before_each('v1', _before_each_v1)
comb.set_after_each('v1', _after_each_v1)

params = {'v1': ['a', 'b'], 'v2': ['A', 'B']}

for _, _ in comb.execute(params):
    pass

# Result
"""
Before v1 a,A
Before each v1 a,A
Execute a,A
Execute a,B
After each v1 a,B
Before each v1 b,A
Execute b,A
Execute b,B
After each v1 b,B
After v1 b,B
"""
