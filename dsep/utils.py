import typing as ty
import itertools

T = ty.TypeVar('T')


def get_max_subsets(
    s: ty.Iterable[T],
    pred: ty.Callable[[tuple[T, ...]], bool],
) -> list[tuple[T, ...]]:
    """
    Find all disjoint max subsets that satisfy a condition. For example,

    >>> def predicate(s):
    ...     return s in map(tuple, 'a b c d ab bc ac'.split())
    >>> get_max_subsets(set('abcd'), predicate)
    [('a', 'b'), ('b', 'c'), ('a', 'c'), ('d',)]

    See tests for more examples.

    :param s: the set of elements
    :param pred: the predicate to check if a subset satisfy the condition
    """
    remaining_combs = []
    for r in range(len(s) + 1):
        curr_combs = list(filter(pred, itertools.combinations(s, r)))
        ind_to_del = []
        for i, x in enumerate(map(set, remaining_combs)):
            for c in map(set, curr_combs):
                if x <= c:
                    ind_to_del.append(i)
                    break
        while ind_to_del:
            del remaining_combs[ind_to_del.pop()]
        remaining_combs.extend(curr_combs)
    return remaining_combs
