"""Combu."""

import itertools
from typing import Any, Callable, cast, Dict, Iterator, List

from combu.combu import Combu
import combu.util

Combu = Combu


class Unset():
    """Unset paramteter."""

    pass


def create_index(params: Dict[str, List[Any]],
                 order: List[str] = None) -> Iterator[Dict[str, int]]:
    """Create parameter index.

    Args:
        params (Dict[str, List[Any]]): Parameters.
        order (List[str], optional): Loop order

    Raises:
        KeyError: Used unknown key on 'order'.

    Yields:
        Iterator[Dict[str, int]]: Index of parameter.
    """
    params_keys = cast(List[str], params.keys())
    keys = combu.util.get_order(params_keys, order=order)

    idx_list = []
    for k in keys:
        # raise KeyError
        param = params[k]
        idx_list.append(
            [-1 if isinstance(v, Unset) else i for i, v in enumerate(param)])

    for comb in itertools.product(*idx_list):
        yield {k: i for k, i in zip(keys, comb) if i >= 0}


def create_value(params: Dict[str, List[Any]],
                 order: List[str] = None) -> Iterator[Dict[str, Any]]:
    """Create parameter value.

    Args:
        params (Dict[str, List[Any]]): Parameters.
        order (List[str], optional): Loop order.

    Raises:
        KeyError: Used unknown key on 'order'.

    Yields:
        Iterator[Dict[str, Any]]: Parameter.
    """
    # raise KeyError
    for comb_idx in create_index(params, order=order):
        yield {k: params[k][i] for k, i in comb_idx.items()}


def execute(func: Callable,
            params: Dict[str, List[Any]],
            order: List[str] = None) -> Iterator[Any]:
    """Execute the function with parameter combination.

    Args:
        func (Callable): Target function.
        params (Dict[str, List[Any]]): Parameters.
        order (List[str], optional): Loop order.

    Raises:
        KeyError: Used unknown key on 'order'.

    Yields:
        Iterator[Any]: Result.
    """
    # raise KeyError
    for comb in create_value(params, order=order):
        yield func(**comb), comb
