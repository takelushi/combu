"""Combu."""

import itertools
from typing import Any, Callable, cast, Dict, Iterable, Iterator, Tuple

from combu.combu import Combu
from combu.definition import Pack, TParams, Unset
import combu.util

Combu = Combu
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
    progress: bool = False,
) -> Iterator[Tuple[Any, Dict[str, Any]]]:
    """Execute the function with parameter combination.

    Args:
        func (Callable): Target function.
        params (TParams): Parameters.
        order (Iterable[TParamsKey], optional): Loop order.
        progress (bool, optional): Show progress bar or not.

    Raises:
        KeyError: Used unknown key on 'order'.
        TypeError: Missing argument.
        TypeError: Unexpected argument.

    Yields:
        Iterator[Tuple[Any, Dict[str, Any]]]: Result and parameter.
    """
    params = cast(TParams, params)

    val_ter = create_values(params, order=order)
    if progress:
        from tqdm.auto import tqdm
        total = combu.util.count(params)
        val_ter = tqdm(val_ter, total=total)

    # raise KeyError
    for comb in val_ter:
        # raise TypeError
        yield func(**comb), comb
