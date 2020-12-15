"""Utility."""

import random
from typing import Any, cast, Dict, List


def get_order(keys: List[str], order: List[str] = None) -> List[str]:
    """Get order.

    Args:
        keys (List[str]): Keys.
        order (List[str], optional): Key order.

    Returns:
        List[str]: [description]
    """
    order = [] if order is None else order
    order += [k for k in keys if k not in order]
    return order


def count(params: Dict[str, List[Any]]) -> int:
    """Count combinations.

    Args:
        params (Dict[str, List[Any]]): Parameters.

    Returns:
        int: Result.
    """
    if params == {}:
        return 0
    result = 1
    for v in params.values():
        result *= len(v)
    return result


def shuffle_params(params: Dict[str, List[Any]],
                   seed: int = None,
                   no_seed: bool = False) -> None:
    """Shuffle parameters.

    Set global seed: random.seed(seed_value)

    Args:
        params (Dict[str, List[Any]]): Parameters.
        seed (int, optional): Seed value.
        no_seed (bool, optional): Do not use global seed or not.
    """
    if no_seed:
        rand = random.Random()
    elif seed is not None:
        rand = random.Random(seed)
    else:
        rand = cast(random.Random, random)

    for k in params.keys():
        rand.shuffle(params[k])
