"""Parallel."""

from multiprocessing import Pool
from typing import Any, Callable, Iterable, Iterator, Tuple

from tqdm.auto import tqdm


class ParallelExecutor:
    """Parallel executor."""

    def __init__(self,
                 target: Callable,
                 n: int = None,
                 progress: bool = False) -> None:
        """Initialize object.

        Args:
            target (Callable): Target function.
            n (int, optional): Number of processes. Default to all cores.
            progress (bool, optional): Show progress bar or not.

        Raises:
            ValueError: n over CPU count.
        """
        self._target = target
        self.n = n
        self.progress = progress

    def _f(self, p) -> Any:
        return self._target(**p)

    def execute(self, params: Iterable[dict]) -> Iterator[Tuple[Any, dict]]:
        """Execute.

        Args:
            params (Iterable[dict]): Parameters.

        Yields:
            Iterator[Tuple[Any, dict]]: Result and parameter.
        """
        params = [param for param in params]  # noqa: C416

        with Pool(self.n) as p:
            jobs = [p.apply_async(self._f, args=[param]) for param in params]
            with tqdm(total=len(jobs), disable=not self.progress) as progress:
                while len(jobs) > 0:
                    for job, param in zip(jobs, params):
                        if job.ready():
                            yield job.get(), param
                            progress.update()
                            jobs.remove(job)
                            params.remove(param)
