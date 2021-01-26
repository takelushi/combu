"""Test generator."""

from typing import Any, List, Tuple

import pytest

import combu.generator as generator


def test_get_order_order() -> None:
    """Test get_order()."""
    patterns: List[List[Any]] = [
        ['a', 'b', 'c'],
        [1],
        [],
    ]
    for pattern in patterns:
        assert generator.get_order(pattern) == pattern


def test_get_order_order_set_order() -> None:
    """Test get_order().

    'order' is set.
    """
    keys = ['a', 'b', 'c']
    patterns: List[Tuple[Any, Any]] = [
        (['c'], ['c', 'a', 'b']),
        (['c', 'b'], ['c', 'b', 'a']),
        (['a', 'b', 'c'], ['a', 'b', 'c']),
        (['c', 'b', 'a'], ['c', 'b', 'a']),
        (['a', 'b', 'c'], ['a', 'b', 'c']),
        ([], keys),
        (None, keys),
    ]
    for order, expected in patterns:
        assert generator.get_order(keys, order=order) == expected


@pytest.mark.skip(reason='Test on execute().')
def test_create_value():
    """Test create_value()."""
    _ = generator.create_values
