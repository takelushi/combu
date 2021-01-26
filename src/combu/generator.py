"""Generator."""

import itertools
from typing import Any, cast, Dict, Iterable, Iterator, List

from combu.definition import TParams, TParamsKey, Unset
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


__all__ = [
    'get_order',
]
