"""Test util."""

import random

import combu.util as util


def test_shuffle_params() -> None:
    """Test shuffle_params()."""
    a = list(range(100))
    b = list(range(100, 0, -1))
    params = {'a': a, 'b': b}
    util.shuffle_params(params)

    assert params['a'] != a
    assert params['b'] != b


def test_shuffle_params_seed() -> None:
    """Test shuffle_params().

    Use seed (Do not use global seed).
    """
    li = list(range(100))

    random.seed(1)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params, seed=5)
    result = params.copy()

    random.seed(2)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params, seed=5)
    assert params == result

    random.seed(1)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params, seed=6)
    assert params != result


def test_shuffle_params_global_seed() -> None:
    """Test shuffle_params().

    Use global seed.
    """
    li = list(range(100))

    random.seed(5)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params)
    result = params.copy()

    random.seed(5)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params)
    assert params == result

    random.seed(6)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params)
    assert params != result


def test_shuffle_params_no_seed() -> None:
    """Test shuffle_params().

    Unable to use global seed.
    """
    li = list(range(100))

    random.seed(5)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params)
    result = params.copy()

    random.seed(5)
    params = {'li': [v for v in li]}  # noqa: C416
    util.shuffle_params(params, no_seed=True)
    assert params != result


def test_count() -> None:
    """Test count()."""
    assert util.count({}) == 0
    assert util.count({'v1': []}) == 0
    assert util.count({'v1': [1], 'v2': []}) == 0

    params = {'v1': [1, 2, 3]}
    assert util.count(params) == 3

    params = {'v1': [1, 2, 3], 'v2': [1, 2]}
    assert util.count(params) == 6
