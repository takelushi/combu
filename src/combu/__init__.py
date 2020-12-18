"""Combu."""

import itertools
from typing import Any, Callable, cast, Dict, Iterator, List, Tuple

from combu.combu import Combu
from combu.definition import TParams, TParamsIndex, TParamsKey, Unset
import combu.util

Combu = Combu
Unset = Unset


def create_index(params: TParams,
                 order: List[str] = None) -> Iterator[TParamsIndex]:
    """Create parameter index.

    Args:
        params (TParams): Parameters.
        order (List[str], optional): Loop order

    Raises:
        KeyError: Used unknown key on 'order'.

    Yields:
        Iterator[TParmsIndex]: Index of parameter.
    """
    params_keys = cast(TParamsKey, params.keys())
    keys = combu.util.get_order(params_keys, order=order)

    idx_list = []
    for k in keys:
        # raise KeyError
        param = params[k]
        idx_list.append(
            [-1 if isinstance(v, Unset) else i for i, v in enumerate(param)])

    for comb in itertools.product(*idx_list):
        yield {k: i for k, i in zip(keys, comb) if i >= 0}


def _unpack_tuple(keys: Tuple[Any, ...], values: Tuple[Any,
                                                       ...]) -> Dict[str, Any]:
    """Unpack tuple.

    Args:
        keys (Tuple[Any, ...]): Keys.
        values (Tuple[Any, ...]): Values.

    Raises:
        ValueError: Unknown key type.

    Returns:
        Dict[str, Any]: Parameter.
    """
    result: Dict[str, Any] = {}
    assert len(keys) == len(values)
    for k, v in zip(keys, values):
        if not isinstance(k, str):
            raise ValueError('Unknown key type.')
        if not isinstance(v, Unset):
            result[k] = v
    return result


def _resolve_params(params: TParams, param_idx: dict) -> Dict[str, Any]:
    """Resolve parameters.

    Args:
        params (TParams): Parameters.
        param_idx (dict): Index of parameter.

    Raises:
        ValueError: Unknown key type.

    Returns:
        Dict[str, Any]: Parameter.
    """
    result: Dict[str, Any] = {}
    for k, i in param_idx.items():
        v = params[k][i]
        if isinstance(k, str):
            result[k] = v
        elif isinstance(k, tuple):
            result = {**result, **_unpack_tuple(k, v)}
        else:
            raise ValueError('Unknown key type.')
    return result


def create_value(params: TParams,
                 order: List[str] = None) -> Iterator[Dict[str, Any]]:
    """Create parameter value.

    Args:
        params (TParams): Parameters.
        order (List[str], optional): Loop order.

    Raises:
        KeyError: Used unknown key on 'order'.

    Yields:
        Iterator[Dict[str, Any]]: Parameter.
    """
    # raise KeyError
    for comb_idx in create_index(params, order=order):
        yield _resolve_params(params, comb_idx)


def execute(func: Callable,
            params: TParams,
            order: List[str] = None) -> Iterator[Any]:
    """Execute the function with parameter combination.

    Args:
        func (Callable): Target function.
        params (TParams): Parameters.
        order (List[str], optional): Loop order.

    Raises:
        KeyError: Used unknown key on 'order'.
        TypeError: Missing argument.
        TypeError: Unexpected argument.

    Yields:
        Iterator[Any]: Result.
    """
    # raise KeyError
    for comb in create_value(params, order=order):
        # raise TypeError
        yield func(**comb), comb
