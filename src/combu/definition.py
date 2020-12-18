"""Definition."""

from typing import Any, Dict, List, Tuple, Union

TParamsKey = Union[str, Tuple[str, ...]]
TParamsValue = Union[List[Any], List[Tuple[Any, ...]]]
TParamsIndex = Dict[TParamsKey, int]
TParams = Dict[TParamsKey, TParamsValue]


class Unset():
    """Unset paramteter."""

    pass
