"""Test combu."""

from typing import Tuple

from combu.combu import Combu


class TestCombu:
    """Test Combu."""

    def test_init(self) -> None:
        """Test initializer."""

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        assert comb.func == func
        assert comb.order == []
        assert comb.before == {}
        assert comb.after == {}
        assert comb.before_each == {}
        assert comb.after_each == {}

    def test_init_kwargs(self) -> None:
        """Test initializer.

        Set keyword arguments.
        """

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        order = ['v2']
        before = {'v1': lambda: print(1)}
        after = {'v1': lambda: print(1)}
        before_each = {'v3': lambda: print(1)}
        after_each = {'v3': lambda: print(1)}
        comb = Combu(
            func,
            order=order,
            before=before,
            after=after,
            before_each=before_each,
            after_each=after_each,
        )
        assert comb.func == func
        assert comb.order == order
        assert comb.before == before
        assert comb.after == after
        assert comb.before_each == before_each
        assert comb.after_each == after_each

    def test_set_before(self) -> None:
        """Test set_before()."""

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        comb.set_before('v1', func)
        assert comb.before == {'v1': func}

    def test_set_after(self) -> None:
        """Test set_after()."""

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        comb.set_after('v1', func)
        assert comb.after == {'v1': func}

    def test_set_before_each(self) -> None:
        """Test set_before_each()."""

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        comb.set_before_each('v1', func)
        assert comb.before_each == {'v1': func}

    def test_set_after_each(self) -> None:
        """Test set_after_each()."""

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        comb.set_after_each('v1', func)
        assert comb.after_each == {'v1': func}

    def test_execute(self) -> None:
        """Test execute()."""

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        params = {
            'v1': [1, 2],
            'v2': ['a', 'b'],
        }
        actual = [res for res in comb.execute(params)]  # noqa: C416
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

    def test_execute_order(self) -> None:
        """Test execute().

        Set 'order'.
        """

        def func(v1: int, v2: str) -> Tuple[int, str]:
            return v1, v2

        comb = Combu(func)
        params = {
            'v1': [1, 2],
            'v2': ['a', 'b'],
        }
        order = ['v2', 'v1']
        gen = comb.execute(params, order=order)
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

    def test_execute_unpack(self) -> None:
        """Test execute().

        Unpack.
        """

        def func(v1: str, v2: int, v3: int) -> Tuple[str, int, int]:
            return v1, v2, v3

        comb = Combu(func)

        params = {
            'v1': ['a', 'b'],
            ('v2', 'v3'): [(0, 0), (1, 1)],
        }
        actual = [res for res in comb.execute(params)]  # noqa: C416
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

    def test_execute_loop_hooks(self) -> None:
        """Test execute().

        Test before, after, before_each, after_each.
        """
        result = []

        def func(v1: str, v2: str) -> None:
            result.append('[func] {},{}'.format(v1, v2))

        comb = Combu(func)

        def before_v1(v1: str, v2: str) -> None:
            result.append('[before.{}] {},{}'.format('v1', v1, v2))

        def after_v1(v1: str, v2: str) -> None:
            result.append('[after.{}] {},{}'.format('v1', v1, v2))

        def before_each_v1(v1: str, v2: str) -> None:
            result.append('[before_each.{}] {},{}'.format('v1', v1, v2))

        def after_each_v1(v1: str, v2: str) -> None:
            result.append('[after_each.{}] {},{}'.format('v1', v1, v2))

        comb.set_before('v1', before_v1)
        comb.set_after('v1', after_v1)
        comb.set_before_each('v1', before_each_v1)
        comb.set_after_each('v1', after_each_v1)

        def before_v2(v1: str, v2: str) -> None:
            result.append('[before.{}] {},{}'.format('v2', v1, v2))

        def after_v2(v1: str, v2: str) -> None:
            result.append('[after.{}] {},{}'.format('v2', v1, v2))

        def before_each_v2(v1: str, v2: str) -> None:
            result.append('[before_each.{}] {},{}'.format('v2', v1, v2))

        def after_each_v2(v1: str, v2: str) -> None:
            result.append('[after_each.{}] {},{}'.format('v2', v1, v2))

        comb.set_before('v2', before_v2)
        comb.set_after('v2', after_v2)
        comb.set_before_each('v2', before_each_v2)
        comb.set_after_each('v2', after_each_v2)

        params = {'v1': ['a'], 'v2': ['A']}
        for _ in comb.execute(params):
            pass

        expected = [
            '[before.v1] a,A',
            '[before.v2] a,A',
            '[before_each.v1] a,A',
            '[before_each.v2] a,A',
            '[func] a,A',
            '[after_each.v2] a,A',
            '[after_each.v1] a,A',
            '[after.v2] a,A',
            '[after.v1] a,A',
        ]

        assert result == expected

    def test_execute_loop_hooks_3(self) -> None:
        """Test execute().

        Test before, after, before_each, after_each.
        """
        result = []

        def func(v1: int, v2: int, v3: int) -> None:
            result.append(['func', v1, v2, v3])

        comb = Combu(func)

        def before_v1(v1: int, v2: int, v3: int) -> None:
            result.append(['before_v1', v1, v2, v3])

        def after_v1(v1: int, v2: int, v3: int) -> None:
            result.append(['after_v1', v1, v2, v3])

        def before_each_v1(v1: int, v2: int, v3: int) -> None:
            result.append(['before_each_v1', v1, v2, v3])

        def after_each_v1(v1: int, v2: int, v3: int) -> None:
            result.append(['after_each_v1', v1, v2, v3])

        comb.set_before('v1', before_v1)
        comb.set_after('v1', after_v1)
        comb.set_before_each('v1', before_each_v1)
        comb.set_after_each('v1', after_each_v1)

        def before_v2(v1: int, v2: int, v3: int) -> None:
            result.append(['before_v2', v1, v2, v3])

        def after_v2(v1: int, v2: int, v3: int) -> None:
            result.append(['after_v2', v1, v2, v3])

        def before_each_v2(v1: int, v2: int, v3: int) -> None:
            result.append(['before_each_v2', v1, v2, v3])

        def after_each_v2(v1: int, v2: int, v3: int) -> None:
            result.append(['after_each_v2', v1, v2, v3])

        comb.set_before('v2', before_v2)
        comb.set_after('v2', after_v2)
        comb.set_before_each('v2', before_each_v2)
        comb.set_after_each('v2', after_each_v2)

        def before_v3(v1: int, v2: int, v3: int) -> None:
            result.append(['before_v3', v1, v2, v3])

        def after_v3(v1: int, v2: int, v3: int) -> None:
            result.append(['after_v3', v1, v2, v3])

        def before_each_v3(v1: int, v2: int, v3: int) -> None:
            result.append(['before_each_v3', v1, v2, v3])

        def after_each_v3(v1: int, v2: int, v3: int) -> None:
            result.append(['after_each_v3', v1, v2, v3])

        comb.set_before('v3', before_v3)
        comb.set_after('v3', after_v3)
        comb.set_before_each('v3', before_each_v3)
        comb.set_after_each('v3', after_each_v3)

        params = {'v1': [1, 2, 3], 'v2': [4, 5, 6], 'v3': [7, 8, 9]}
        for _ in comb.execute(params):
            pass
        expected = [
            ['before_v1', 1, 4, 7],
            ['before_v2', 1, 4, 7],
            ['before_v3', 1, 4, 7],
            ['before_each_v1', 1, 4, 7],
            ['before_each_v2', 1, 4, 7],
            ['before_each_v3', 1, 4, 7],
            ['func', 1, 4, 7],
            ['after_each_v3', 1, 4, 7],
            ['before_each_v3', 1, 4, 8],
            ['func', 1, 4, 8],
            ['after_each_v3', 1, 4, 8],
            ['before_each_v3', 1, 4, 9],
            ['func', 1, 4, 9],
            ['after_each_v3', 1, 4, 9],
            ['after_each_v2', 1, 4, 9],
            ['before_v3', 1, 5, 7],
            ['before_each_v2', 1, 5, 7],
            ['before_each_v3', 1, 5, 7],
            ['func', 1, 5, 7],
            ['after_each_v3', 1, 5, 7],
            ['before_each_v3', 1, 5, 8],
            ['func', 1, 5, 8],
            ['after_each_v3', 1, 5, 8],
            ['before_each_v3', 1, 5, 9],
            ['func', 1, 5, 9],
            ['after_each_v3', 1, 5, 9],
            ['after_each_v2', 1, 5, 9],
            ['before_v3', 1, 6, 7],
            ['before_each_v2', 1, 6, 7],
            ['before_each_v3', 1, 6, 7],
            ['func', 1, 6, 7],
            ['after_each_v3', 1, 6, 7],
            ['before_each_v3', 1, 6, 8],
            ['func', 1, 6, 8],
            ['after_each_v3', 1, 6, 8],
            ['before_each_v3', 1, 6, 9],
            ['func', 1, 6, 9],
            ['after_each_v3', 1, 6, 9],
            ['after_each_v2', 1, 6, 9],
            ['after_each_v1', 1, 6, 9],
            ['after_v3', 1, 6, 9],
            ['after_v2', 1, 6, 9],
            ['before_v2', 2, 4, 7],
            ['before_v3', 2, 4, 7],
            ['before_each_v1', 2, 4, 7],
            ['before_each_v2', 2, 4, 7],
            ['before_each_v3', 2, 4, 7],
            ['func', 2, 4, 7],
            ['after_each_v3', 2, 4, 7],
            ['before_each_v3', 2, 4, 8],
            ['func', 2, 4, 8],
            ['after_each_v3', 2, 4, 8],
            ['before_each_v3', 2, 4, 9],
            ['func', 2, 4, 9],
            ['after_each_v3', 2, 4, 9],
            ['after_each_v2', 2, 4, 9],
            ['before_v3', 2, 5, 7],
            ['before_each_v2', 2, 5, 7],
            ['before_each_v3', 2, 5, 7],
            ['func', 2, 5, 7],
            ['after_each_v3', 2, 5, 7],
            ['before_each_v3', 2, 5, 8],
            ['func', 2, 5, 8],
            ['after_each_v3', 2, 5, 8],
            ['before_each_v3', 2, 5, 9],
            ['func', 2, 5, 9],
            ['after_each_v3', 2, 5, 9],
            ['after_each_v2', 2, 5, 9],
            ['before_v3', 2, 6, 7],
            ['before_each_v2', 2, 6, 7],
            ['before_each_v3', 2, 6, 7],
            ['func', 2, 6, 7],
            ['after_each_v3', 2, 6, 7],
            ['before_each_v3', 2, 6, 8],
            ['func', 2, 6, 8],
            ['after_each_v3', 2, 6, 8],
            ['before_each_v3', 2, 6, 9],
            ['func', 2, 6, 9],
            ['after_each_v3', 2, 6, 9],
            ['after_each_v2', 2, 6, 9],
            ['after_each_v1', 2, 6, 9],
            ['after_v3', 2, 6, 9],
            ['after_v2', 2, 6, 9],
            ['before_v2', 3, 4, 7],
            ['before_v3', 3, 4, 7],
            ['before_each_v1', 3, 4, 7],
            ['before_each_v2', 3, 4, 7],
            ['before_each_v3', 3, 4, 7],
            ['func', 3, 4, 7],
            ['after_each_v3', 3, 4, 7],
            ['before_each_v3', 3, 4, 8],
            ['func', 3, 4, 8],
            ['after_each_v3', 3, 4, 8],
            ['before_each_v3', 3, 4, 9],
            ['func', 3, 4, 9],
            ['after_each_v3', 3, 4, 9],
            ['after_each_v2', 3, 4, 9],
            ['before_v3', 3, 5, 7],
            ['before_each_v2', 3, 5, 7],
            ['before_each_v3', 3, 5, 7],
            ['func', 3, 5, 7],
            ['after_each_v3', 3, 5, 7],
            ['before_each_v3', 3, 5, 8],
            ['func', 3, 5, 8],
            ['after_each_v3', 3, 5, 8],
            ['before_each_v3', 3, 5, 9],
            ['func', 3, 5, 9],
            ['after_each_v3', 3, 5, 9],
            ['after_each_v2', 3, 5, 9],
            ['before_v3', 3, 6, 7],
            ['before_each_v2', 3, 6, 7],
            ['before_each_v3', 3, 6, 7],
            ['func', 3, 6, 7],
            ['after_each_v3', 3, 6, 7],
            ['before_each_v3', 3, 6, 8],
            ['func', 3, 6, 8],
            ['after_each_v3', 3, 6, 8],
            ['before_each_v3', 3, 6, 9],
            ['func', 3, 6, 9],
            ['after_each_v3', 3, 6, 9],
            ['after_each_v2', 3, 6, 9],
            ['after_each_v1', 3, 6, 9],
            ['after_v3', 3, 6, 9],
            ['after_v2', 3, 6, 9],
            ['after_v1', 3, 6, 9],
        ]
        assert result == expected
