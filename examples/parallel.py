"""Parallel."""

import time

import combu


def _f(v1, v2):
    time.sleep(0.5)
    return v1 * v2


params_a = {'v1': range(1, 3), 'v2': range(1, 3)}
start_time = time.monotonic()
for _, _ in combu.execute(_f, params_a, n_jobs=4, progress=True):
    pass

print('Total time: {:.2f} s'.format(time.monotonic() - start_time))

comb = combu.CombuParallel(_f, n_jobs=4, progress=True)
params_b = {'v1': [1, 10, 100], 'v2': range(1, 11)}
start_time = time.monotonic()
for _, _ in comb.execute(params_b):
    pass

print('Total time: {:.2f} s'.format(time.monotonic() - start_time))

# Result
"""
100%|██████████████████████████████████████████| 4/4 [00:00<00:00,  7.53it/s]
Total time: 0.56s
100%|████████████████████████████████████████| 30/30 [00:04<00:00,  7.44it/s]
Total time: 4.04s
"""
