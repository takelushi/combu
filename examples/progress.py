"""Progress."""

import time

import combu


def _f(v1, v2):
    time.sleep(0.1)
    return v1 * v2


params_a = {'v1': range(1, 3), 'v2': range(1, 3)}
for _, _ in combu.execute(_f, params_a, progress=True):
    pass

comb = combu.Combu(_f, progress=True)

params_b = {'v1': [1, 10, 100], 'v2': range(1, 11)}
for _, _ in comb.execute(params_b):
    pass

# Result
"""
100%|██████████████████████████████████████| 4/4 [00:00<00:00,  9.95it/s]
100%|████████████████████████████████████| 30/30 [00:03<00:00,  9.94it/s]
"""
