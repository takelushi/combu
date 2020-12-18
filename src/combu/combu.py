"""Combu."""

import itertools
from typing import Any, Callable, cast, Dict, Iterator, List, Tuple

import combu
from combu.definition import TParams, TParamsKey, Unset
import combu.util


def _create_comb_index(
    params: Dict[TParamsKey, List],
    order: List[TParamsKey] = None,
) -> Iterator[Dict[TParamsKey, int]]:
    """Create parameter index.

    Args:
        params (Dict[TParamsKey, List]): Parameters.
        order (List[TParamsKey], optional): Loop order.

    Raises:
        KeyError: Used unknown key on 'order'.

    Yields:
        Iterator[Dict[TParamsKey, int]]: Index of parameter.
    """
    keys = combu.util.get_order(params.keys(), order=order)  # type: ignore
    idx_list = []
    for k in keys:
        # raise KeyError
        param = params[k]
        idx_list.append([i for i in range(len(param))])  # noqa: C416

    for comb in itertools.product(*idx_list):
        yield {k: i for k, i in zip(keys, comb) if i >= 0}


def _merge_dict(*d_li) -> dict:
    """Merge dict.

    Returns:
        dict: Merged dict.
    """
    result: dict = {}

    for d in d_li:
        result = {**result, **d}
    return result


class Combu:
    """Combination parameter.

    [Loop hooks system]
    order = [A, B]

    before_a()
    for a in A:
        before_b()
        before_each_a()
        for b in B:
            before_each_b()
            func()
            after_each_b()
        after_each_a()
        after_b()
    after_a()
    """

    def __init__(self,
                 func: Callable,
                 order: List[TParamsKey] = None,
                 before: Dict[str, Callable] = None,
                 after: Dict[str, Callable] = None,
                 before_each: Dict[str, Callable] = None,
                 after_each: Dict[str, Callable] = None) -> None:
        """Initialize object.

        Args:
            func (Callable): Target function.
            order (List[TParamsKey], optional): Loop order.
            before (Dict[str, Callable], optional): Functions before loop.e.
            after (Dict[str, Callable], optional): Functions after loop.
            before_each (Dict[str, Callable], optional):
                Functions before each loops.
            after_each (Dict[str, Callable], optional):
                Functions after each loops.
        """
        self.func = func
        self.order = [] if order is None else order
        self.before = {} if before is None else before
        self.after = {} if after is None else after
        self.before_each = {} if before_each is None else before_each
        self.after_each = {} if after_each is None else after_each

    def set_before(self, k: str, func: Callable) -> None:
        """Set before function.

        Args:
            k (str): Key.
            func (Callable): Function.
        """
        self.before[k] = func

    def set_after(self, k: str, func: Callable) -> None:
        """Set after function.

        Args:
            k (str): Key.
            func (Callable): Function.
        """
        self.after[k] = func

    def set_before_each(self, k: str, func: Callable) -> None:
        """Set before each function.

        Args:
            k (str): Key.
            func (Callable): Function.
        """
        self.before_each[k] = func

    def set_after_each(self, k: str, func: Callable) -> None:
        """Set after each function.

        Args:
            k (str): Key.
            func (Callable): Function.
        """
        self.after_each[k] = func

    def execute(
        self,
        params: TParams,
        order: List[TParamsKey] = None,
    ) -> Iterator[Tuple[Any, Dict[str, Any]]]:
        """Execute the function.

        Args:
            params (TParams): Parameters.
            order (List[TParamsKey], optional): Loop order.

        Raises:
            KeyError: Unknown key.

        Yields:
            Iterator[Tuple[Any, Dict[str, Any]]]: Result.
        """
        if order is None:
            order = self.order

        params_keys = cast(List[TParamsKey], params.keys())
        order = combu.util.get_order(params_keys, order=order)

        combs_list = combu.util.standardize(params, order=order)
        combs = {k: comb for k, comb in zip(order, combs_list)}

        before_idx = {k: -1 for k in order}
        last_param_idx = {k: len(combs[k]) - 1 for k in order}

        for comb_idx in _create_comb_index(combs):
            comb = [combs[k][i] for k, i in comb_idx.items()]  # type: ignore
            param = _merge_dict(*comb)
            param = {
                k: v for k, v in param.items() if not isinstance(v, Unset)
            }

            # Before loop
            for k in self.before.keys():
                if comb_idx[k] == 0 and before_idx[k] != 0:
                    self.before[k](**param)

            # Before each loop
            for k in self.before_each.keys():
                if comb_idx[k] != before_idx[k]:
                    self.before_each[k](**param)

            yield self.func(**param), param

            # After each loop
            for k in reversed(list(self.after_each.keys())):
                keys = order[order.index(k) + 1:]
                if all(comb_idx[k] == last_param_idx[k] for k in keys):
                    self.after_each[k](**param)

            # After loop
            for k in reversed(list(self.after.keys())):
                if comb_idx[k] == last_param_idx[k]:
                    if all(comb_idx[k] == last_param_idx[k] for k in keys):
                        self.after[k](**param)

            before_idx = comb_idx
