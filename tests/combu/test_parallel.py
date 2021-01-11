"""Test parallel."""

import time

from combu.parallel import ParallelExecutor


def _f(v):
    return v


def _wait(v):
    time.sleep(v)
    return v


class TestParallelExecutor:
    """Test ParallelExecutor class."""

    def test_init(self) -> None:
        """Test __init__()."""
        parallel = ParallelExecutor(_f)
        assert parallel._target == _f

        parallel = ParallelExecutor(_f, n=2, progress=True)
        assert parallel._target == _f
        assert parallel.n == 2
        assert parallel.progress  # == True

    def test_execute(self) -> None:
        """Test execute()."""
        parallel = ParallelExecutor(_f)
        params = [{'v': 1}, {'v': 2}, {'v': 3}]

        results = []
        for res, param in parallel.execute(params):
            # Match parameter and result.
            assert res == param['v']
            results.append(res)

        assert len(results) == 3
        assert 1 in results
        assert 2 in results
        assert 3 in results

    def test_execute_time(self) -> None:
        """Test execute().

        Check parallel or not with time.
        """
        t = 0.1
        params = [{'v': t} for _ in range(12)]

        parallel = ParallelExecutor(_wait, n=2)
        start_time = time.monotonic()
        results = [res for res, _ in parallel.execute(params)]
        total_time = time.monotonic() - start_time
        # Results.
        assert results == [t] * len(params)
        # Time.
        assert total_time < t * len(params)

    def test_execute_single(self) -> None:
        """Test execute().

        Single process.
        """
        t = 0.1
        params = [{'v': t} for _ in range(10)]

        parallel = ParallelExecutor(_wait, n=1)
        start_time = time.monotonic()
        for _, _ in parallel.execute(params):
            pass
        total_time = time.monotonic() - start_time

        assert t * len(params) < total_time + 0.5
        assert t * len(params) > total_time - 0.5

    def test_pass_f(self) -> None:
        """Pass _f().

        This is a not text case.
        """
        parallel = ParallelExecutor(_f)
        parallel._f({'v': 1})
