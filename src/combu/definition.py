"""Definition."""

from typing import Any, Dict, Iterable, Tuple, Union


class Unset():
    """Unset paramteter."""

    pass


class Pack():
    """Packed combination parameter."""

    def __init__(self, *keys: str) -> None:
        """Initialize object."""
        self.keys = [k for k in keys]  # noqa: C416


TParamsKey = Union[str, Tuple[str, ...]]
TParamsValue = Union[Iterable[Any], Iterable[Tuple[Any, ...]], Pack]
TParams = Dict[TParamsKey, Iterable[TParamsValue]]
