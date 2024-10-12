import typing as ty
import itertools

from dsep import utils as m

T = ty.TypeVar('T')


def enum_predicate(*elements: T) -> ty.Callable[[T], bool]:
    """
    A predicate that returns ``True`` iff the input is in ``elements``.
    """
    def _predicate(x):
        return x in elements

    return _predicate


def str_to_tuples(string: str) -> ty.Iterator[tuple[str, ...]]:
    if not string:
        return iter([])
    return map(tuple, string.split())


class TestGetMaxSubsets:
    def test_empty_set(self):
        assert m.get_max_subsets(set(), lambda _: True) == [()]

    def test_none_satisfied(self):
        assert m.get_max_subsets('xyz', enum_predicate()) == []

    def test_all_satisfied(self):
        all_combs = itertools.chain.from_iterable(
            itertools.combinations('xyz', r) for r in [1, 2, 3])
        assert set(m.get_max_subsets('xyz', enum_predicate(*all_combs))) == {
            ('x', 'y', 'z')
        }

    def test_basic(self):
        assert set(
            m.get_max_subsets(
                'abcd',
                enum_predicate(*str_to_tuples('a b c d ab bc ac')))) == {
                    ('a', 'b'), ('b', 'c'), ('a', 'c'), ('d',)
                }

    def test_cases(self):
        cases = [
            'y',
            'xyz',
            'y z wy',
            'wy wxz',
            'wx wyz wxyz',
            'w z x wx wxy',
            'w wz yz wyz xyz',
            'y w yz xz wxz wyz',
            'y xy wx xyz wyz wxyz',
            'z w wx xz xyz wyz wxy',
            'w y yz wx wz xy wxz xyz',
            'z xz xy wxz wyz xyz wxyz',
            'y x w wy yz xz wz xyz wyz wxy',
            'x w z wz wy yz xy wx xyz wxy wyz',
            'w y x xy wy wx yz xz wxy wyz wxyz',
            'y w z x wz yz xy wx wy xz xyz wxz',
            'y x wz xz yz xy wx wy wxz xyz wxy',
            'z w wx xy xz wy yz wxy xyz wxz wxyz',
        ]
        assert [
            set(m.get_max_subsets('wxyz', enum_predicate(*str_to_tuples(c))))
            for c in cases
        ] == [
            {('y',)},
            {('x', 'y', 'z')},
            {('z',), ('w', 'y')},
            {('w', 'y'), ('w', 'x', 'z')},
            {('w', 'x', 'y', 'z')},
            {('z',), ('w', 'x', 'y')},
            {('w', 'y', 'z'), ('x', 'y', 'z')},
            {('w', 'x', 'z'), ('w', 'y', 'z')},
            {('w', 'x', 'y', 'z')},
            {('x', 'y', 'z'), ('w', 'y', 'z'), ('w', 'x', 'y')},
            {('w', 'x', 'z'), ('x', 'y', 'z')},
            {('w', 'x', 'y', 'z')},
            {('x', 'y', 'z'), ('w', 'y', 'z'), ('w', 'x', 'y')},
            {('x', 'y', 'z'), ('w', 'x', 'y'), ('w', 'y', 'z')},
            {('w', 'x', 'y', 'z')},
            {('w', 'y'), ('x', 'y', 'z'), ('w', 'x', 'z')},
            {('w', 'x', 'z'), ('x', 'y', 'z'), ('w', 'x', 'y')},
            {('w', 'x', 'y', 'z')},
        ]
