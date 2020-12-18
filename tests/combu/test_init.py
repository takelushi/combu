"""Test __init__.py."""

from typing import Tuple

import combu
from combu.combu import Combu
from combu.definition import Pack, Unset
import pytest


def test_import_combu_class():
    """Test import Combu class."""
    assert combu.Combu == Combu


def test_import_unset_class():
    """Test import Unset class."""
    assert combu.Unset == Unset


def test_import_pack_class():
    """Test import Pack class."""
    assert combu.Pack == Pack


@pytest.mark.skip(reason='Test on execute().')
def test_create_index():
    """Test create_index()."""
    pass


@pytest.mark.skip(reason='Test on execute().')
def test_create_value():
    """Test create_value()."""
    pass


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


def test_execute_missing_arg() -> None:
    """Test execute().

    Missing argument.
    """

    def func(v1: int, v2: str) -> Tuple[int, str]:
        return v1, v2

    params = {
        'v1': [1, 2],
    }
    with pytest.raises(TypeError):
        for _ in combu.execute(func, params):
            pass


def test_execute_unexpected_arg() -> None:
    """Test execute().

    Unexpected argument.
    """

    def func(v1: int) -> int:
        return v1

    params = {'v1': [1, 2], 'v2': ['a', 'b']}
    with pytest.raises(TypeError):
        for _ in combu.execute(func, params):
            pass


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


def test_execute_unset() -> None:
    """Test execute().

    Use Unset.
    """

    def func(v1: int, v2: str = 'default') -> Tuple[int, str]:
        return v1, v2

    params = {
        'v1': [1, 2],
        'v2': ['a', Unset()],
    }
    actual = [res for res in combu.execute(func, params)]  # noqa: C416
    expected_list = [
        ((1, 'a'), {
            'v1': 1,
            'v2': 'a',
        }),
        ((1, 'default'), {
            'v1': 1,
        }),
        ((2, 'a'), {
            'v1': 2,
            'v2': 'a',
        }),
        ((2, 'default'), {
            'v1': 2,
        }),
    ]
    assert actual == expected_list


def test_execute_unpack_tuple() -> None:
    """Test execute().

    Unpack tuple.
    """

    def func(v1: str, v2: int, v3: int) -> Tuple[str, int, int]:
        return v1, v2, v3

    params = {
        'v1': ['a', 'b'],
        ('v2', 'v3'): [(0, 0), (1, 1)],
    }
    actual = [res for res in combu.execute(func, params)]  # noqa: C416
    expected_list = [
        (('a', 0, 0), {
            'v1': 'a',
            'v2': 0,
            'v3': 0,
        }),
        (('a', 1, 1), {
            'v1': 'a',
            'v2': 1,
            'v3': 1,
        }),
        (('b', 0, 0), {
            'v1': 'b',
            'v2': 0,
            'v3': 0,
        }),
        (('b', 1, 1), {
            'v1': 'b',
            'v2': 1,
            'v3': 1,
        }),
    ]
    assert actual == expected_list


def test_execute_unpack_tuple_wrong_key_type() -> None:
    """Test execute().

    Wrong key type on unpack tuple.
    """

    def func(v1: int, v2: str) -> Tuple[int, str]:
        return v1, v2

    params = {('v1', 123): [(1, 'a')]}

    with pytest.raises(TypeError):
        for _ in combu.execute(func, params):
            pass


def test_execute_unpack_pack() -> None:
    """Test execute().

    Unpack pack.
    """

    def func(v1: str, v2: int, v3: int) -> Tuple[str, int, int]:
        return v1, v2, v3

    params = {
        'v1': ['a', 'b'],
        Pack('v2', 'v3'): [{
            'v2': [0, 1],
            'v3': [0, 1],
        }, {
            'v2': [2, 3],
            'v3': [2, 3],
        }],
    }
    actual = [res for res in combu.execute(func, params)]  # noqa: C416
    expected_list = [
        (('a', 0, 0), {
            'v1': 'a',
            'v2': 0,
            'v3': 0,
        }),
        (('a', 0, 1), {
            'v1': 'a',
            'v2': 0,
            'v3': 1,
        }),
        (('a', 1, 0), {
            'v1': 'a',
            'v2': 1,
            'v3': 0,
        }),
        (('a', 1, 1), {
            'v1': 'a',
            'v2': 1,
            'v3': 1,
        }),
        (('a', 2, 2), {
            'v1': 'a',
            'v2': 2,
            'v3': 2,
        }),
        (('a', 2, 3), {
            'v1': 'a',
            'v2': 2,
            'v3': 3,
        }),
        (('a', 3, 2), {
            'v1': 'a',
            'v2': 3,
            'v3': 2,
        }),
        (('a', 3, 3), {
            'v1': 'a',
            'v2': 3,
            'v3': 3,
        }),
        (('b', 0, 0), {
            'v1': 'b',
            'v2': 0,
            'v3': 0,
        }),
        (('b', 0, 1), {
            'v1': 'b',
            'v2': 0,
            'v3': 1,
        }),
        (('b', 1, 0), {
            'v1': 'b',
            'v2': 1,
            'v3': 0,
        }),
        (('b', 1, 1), {
            'v1': 'b',
            'v2': 1,
            'v3': 1,
        }),
        (('b', 2, 2), {
            'v1': 'b',
            'v2': 2,
            'v3': 2,
        }),
        (('b', 2, 3), {
            'v1': 'b',
            'v2': 2,
            'v3': 3,
        }),
        (('b', 3, 2), {
            'v1': 'b',
            'v2': 3,
            'v3': 2,
        }),
        (('b', 3, 3), {
            'v1': 'b',
            'v2': 3,
            'v3': 3,
        }),
    ]
    assert actual == expected_list


def test_execute_wrong_key_type() -> None:
    """Test execute().

    Wrong key type.
    """

    def func(v1: int, v2: str) -> Tuple[int, str]:
        return v1, v2

    params = {
        'v1': [1, 2],
        123: ['a', 'b'],
    }

    with pytest.raises(TypeError):
        for _ in combu.execute(func, params):
            pass
