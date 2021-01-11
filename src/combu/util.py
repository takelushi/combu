"""Utility."""

import random
from typing import Any, cast, Dict, Iterable, List, Tuple

import combu
from combu.definition import Pack, TParams, TParamsKey, TParamsValue
import combu.util


def get_order(keys: Iterable[TParamsKey],
              order: Iterable[TParamsKey] = None) -> List[TParamsKey]:
    """Get order.

    Args:
        keys (Iterable[TParamsKey]): Keys.
        order (Iterable[TParamsKey], optional): Key order.

    Returns:
        List[TParamsKey]: Keys order.
    """
    order = [] if order is None else [k for k in order]  # noqa: C416
    order += [k for k in keys if k not in order]
    return order


def _unpack_tuple(keys: Tuple[Any, ...],
                  vals_l: Iterable[Tuple[Any, ...]]) -> List[Dict[str, Any]]:
    result = []
    for k in keys:
        if not isinstance(k, str):
            raise TypeError('Wrong tuple value type.')
    for vals in vals_l:
        assert len(keys) == len(vals)
        result.append({k: v for k, v in zip(keys, vals)})
    return result


def _unpack_pack(pack: Pack, params_iter: Iterable[TParams]):
    result = []
    for k in pack.keys:
        assert isinstance(k, str)
    for params in params_iter:
        keys = cast(Iterable[str], pack.keys)
        vals = combu.create_values(params, order=keys)
        result += [v for v in vals]  # noqa: C416

    return result


def _unpack(k: TParamsKey, v: Iterable[TParamsValue]) -> List[Dict[str, Any]]:
    if isinstance(k, str):
        return [{k: sub_v} for sub_v in v]
    elif isinstance(k, tuple):
        return _unpack_tuple(k, v)  # type: ignore
    elif isinstance(k, Pack):
        return _unpack_pack(k, v)  # type: ignore
    else:
        raise TypeError('Unknown key type.')


def standardize(
        params: TParams,
        order: Iterable[TParamsKey] = None) -> List[List[Dict[str, Any]]]:
    """Standardize parameters.

    Args:
        params (TParams): Parameters.
        order (Iterable[TParamsKey], optional): Key order.

    Returns:
        List[List[Dict[str, Any]]]: Standardized parameters.
    """
    keys = combu.util.get_order(params.keys(), order=order)

    results = []

    for k in keys:
        results.append(_unpack(k, params[k]))
    return results


def count(params: dict) -> int:
    """Count combinations.

    Args:
        params (TParams): Parameters.

    Returns:
        int: Result.
    """
    params = cast(TParams, params)
    if params == {}:
        return 0
    result = 1
    for v in standardize(params):
        result *= len(v)
    return result


def shuffle_params(params: dict,
                   seed: int = None,
                   no_seed: bool = False) -> None:
    """Shuffle parameters.

    Set global seed: random.seed(seed_value)

    Args:
        params (Dict[str, Iterable[Any]]): Parameters.
        seed (int, optional): Seed value.
        no_seed (bool, optional): Do not use global seed or not.
    """
    params = cast(Dict[str, Iterable[Any]], params)

    if no_seed:
        rand = random.Random()
    elif seed is not None:
        rand = random.Random(seed)
    else:
        rand = cast(random.Random, random)

    for k in params.keys():
        vals = [v for v in params[k]]  # noqa: C416
        rand.shuffle(vals)
        params[k] = vals
