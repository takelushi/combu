"""Execute combination parameter."""

from typing import Any, Callable, cast, Dict, Iterable, Iterator, Tuple

from combu.definition import TParams
from combu.generator import create_values
from combu.parallel import ParallelExecutor
import combu.util


def execute(
    func: Callable,
    params: dict,
    order: Iterable = None,
    n_jobs: int = 1,
    progress: bool = False,
) -> Iterator[Tuple[Any, Dict[str, Any]]]:
    """Execute the function with parameter combination.

    Args:
        func (Callable): Target function.
        params (TParams): Parameters.
        order (Iterable[TParamsKey], optional): Loop order.
        n_jobs (int, optional): Number of processes. Default to 1.
        progress (bool, optional): Show progress bar or not.

    Raises:
        KeyError: Used unknown key on 'order'.
        TypeError: Missing argument.
        TypeError: Unexpected argument.

    Yields:
        Iterator[Tuple[Any, Dict[str, Any]]]: Result and parameter.
    """
    params = cast(TParams, params)

    val_iter = create_values(params, order=order)

    if n_jobs == 1:
        if progress:
            from tqdm.auto import tqdm
            total = combu.util.count(params)
            val_iter = tqdm(val_iter, total=total)

        # raise KeyError
        for comb in val_iter:
            # raise TypeError
            yield func(**comb), comb
    else:
        n = None if n_jobs < 0 else n_jobs
        parallel = ParallelExecutor(func, n=n, progress=progress)
        for res, param in parallel.execute(val_iter):
            yield res, param
