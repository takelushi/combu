"""Definition."""

from typing import Any, Dict, List, Tuple, Union


class Unset():
    """Unset paramteter."""

    pass


class Pack():
    """Packed combination parameter."""

    def __init__(self, *keys: List[str]) -> None:
        """Initialize object."""
        self.keys = list(keys)


TParamsKey = Union[str, Tuple[str, ...]]
TParamsValue = Union[List[Any], List[Tuple[Any, ...]], Pack]
TParams = Dict[TParamsKey, List[TParamsValue]]
