"""Combu."""

import itertools
from typing import Any, Callable, cast, Dict, Iterable, Iterator, Tuple

from combu.combu import Combu, CombuParallel
from combu.definition import Pack, TParams, Unset
from combu.parallel import ParallelExecutor
import combu.util

Combu = Combu
CombuParallel = CombuParallel
Pack = Pack
Unset = Unset


def create_values(params: dict,
                  order: Iterable = None) -> Iterator[Dict[str, Any]]:
    """Create values.

    Args:
        params (TParams): Parameters.
        order (Iterable[ParamsKey], optional): Key order.

    Yields:
        Iterator[Dict[str, Any]]: Parameter.
    """
    params = cast(TParams, params)
    combs_list = combu.util.standardize(params, order=order)
    for combs in itertools.product(*combs_list):
        param: Dict[str, Any] = {}
        for comb in combs:
            param = {**param, **comb}
        yield {k: v for k, v in param.items() if not isinstance(v, Unset)}


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
