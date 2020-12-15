"""Test __init__.py."""

from typing import Tuple

import combu
from combu.combu import Combu


def test_import_combu_class():
    """Test import Combu class."""
    assert combu.Combu == Combu


def test_create_index():
    """Test create_index()."""
    params = {'v1': ['a', 'b'], 'v2': ['x', 'y']}
    actual = [res for res in combu.create_index(params)]  # noqa: C416
    expected = [
        {
            'v1': 0,
            'v2': 0,
        },
        {
            'v1': 0,
            'v2': 1,
        },
        {
            'v1': 1,
            'v2': 0,
        },
        {
            'v1': 1,
            'v2': 1,
        },
    ]

    assert actual == expected


def test_create_index_order():
    """Test create_index().

    Set 'order'.
    """
    params = {'v1': ['a', 'b'], 'v2': ['x', 'y']}
    order = ['v2', 'v1']
    gen = combu.create_index(params, order=order)
    actual = [res for res in gen]  # noqa: C416
    expected = [
        {
            'v1': 0,
            'v2': 0,
        },
        {
            'v1': 1,
            'v2': 0,
        },
        {
            'v1': 0,
            'v2': 1,
        },
        {
            'v1': 1,
            'v2': 1,
        },
    ]

    assert actual == expected


def test_create_value():
    """Test create_value()."""
    params = {'v1': ['a', 'b'], 'v2': ['x', 'y']}
    actual = [res for res in combu.create_value(params)]  # noqa: C416
    expected = [
        {
            'v1': 'a',
            'v2': 'x',
        },
        {
            'v1': 'a',
            'v2': 'y',
        },
        {
            'v1': 'b',
            'v2': 'x',
        },
        {
            'v1': 'b',
            'v2': 'y',
        },
    ]

    assert actual == expected


def test_create_value_order():
    """Test create_value().

    Set 'order'.
    """
    params = {'v1': ['a', 'b'], 'v2': ['x', 'y']}
    order = ['v2', 'v1']
    gen = combu.create_value(params, order=order)
    actual = [res for res in gen]  # noqa: C416
    expected = [
        {
            'v1': 'a',
            'v2': 'x',
        },
        {
            'v1': 'b',
            'v2': 'x',
        },
        {
            'v1': 'a',
            'v2': 'y',
        },
        {
            'v1': 'b',
            'v2': 'y',
        },
    ]

    assert actual == expected


def test_execute() -> None:
    """Test execute()."""

    def func(v1: int, v2: str) -> Tuple[int, str]:
        return v1, v2

    params = {
        'v1': [1, 2],
        'v2': ['a', 'b'],
    }
    actual = [res for res in combu.execute(func, params)]  # noqa: C416
    expected_list = [
        ((1, 'a'), {
            'v1': 1,
            'v2': 'a',
        }),
        ((1, 'b'), {
            'v1': 1,
            'v2': 'b',
        }),
        ((2, 'a'), {
            'v1': 2,
            'v2': 'a',
        }),
        ((2, 'b'), {
            'v1': 2,
            'v2': 'b',
        }),
    ]
    assert actual == expected_list


def test_execute_order() -> None:
    """Test execute().

    Set 'order'.
    """

    def func(v1: int, v2: str) -> Tuple[int, str]:
        return v1, v2

    params = {
        'v1': [1, 2],
        'v2': ['a', 'b'],
    }
    order = ['v2', 'v1']
    gen = combu.execute(func, params, order=order)
    actual = [res for res in gen]  # noqa: C416
    expected_list = [
        ((1, 'a'), {
            'v1': 1,
            'v2': 'a',
        }),
        ((2, 'a'), {
            'v1': 2,
            'v2': 'a',
        }),
        ((1, 'b'), {
            'v1': 1,
            'v2': 'b',
        }),
        ((2, 'b'), {
            'v1': 2,
            'v2': 'b',
        }),
    ]
    assert actual == expected_list
