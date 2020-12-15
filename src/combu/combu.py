"""Combu."""

from typing import Any, Callable, cast, Dict, Iterator, List

import combu


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
                 order: List[str] = None,
                 before: Dict[str, Callable] = None,
                 after: Dict[str, Callable] = None,
                 before_each: Dict[str, Callable] = None,
                 after_each: Dict[str, Callable] = None) -> None:
        """Initialize object.

        Args:
            func (Callable): Target function.
            order (List[str], optional): Loop order.
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

    def execute(self,
                params: Dict[str, List[Any]],
                order: List[str] = None) -> Iterator[Any]:
        """Execute the function.

        Args:
            params (Dict[str, List[Any]]): Parameters.
            order (List[str], optional): Loop order.

        Raises:
            KeyError: Unknown key.

        Yields:
            Iterator[Any]: Result.
        """
        params_keys = cast(List[str], params.keys())
        order = combu.util.get_order(params_keys, order=order)
        before_idx = {k: -1 for k in params.keys()}
        last_param_idx = {k: len(v) - 1 for k, v in params.items()}

        # raise KeyError
        for comb_idx in combu.create_index(params, order=order):
            comb = {k: params[k][i] for k, i in comb_idx.items()}

            # Before loop
            for k in self.before.keys():
                if comb_idx[k] == 0 and before_idx[k] != 0:
                    self.before[k](**comb)

            # Before each loop
            for k in self.before_each.keys():
                if comb_idx[k] != before_idx[k]:
                    self.before_each[k](**comb)

            yield self.func(**comb), comb

            # After each loop
            for k in reversed(list(self.after_each.keys())):
                keys = order[order.index(k) + 1:]
                if all(comb_idx[k] == last_param_idx[k] for k in keys):
                    self.after_each[k](**comb)

            # After loop
            for k in reversed(list(self.after.keys())):
                if comb_idx[k] == last_param_idx[k]:
                    if all(comb_idx[k] == last_param_idx[k] for k in keys):
                        self.after[k](**comb)

            before_idx = comb_idx
