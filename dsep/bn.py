"""
D-separation of Bayesian networks.
"""

import networkx as nx
from networkx.algorithms.d_separation import is_d_separator

from dsep import utils


def check_conditional_independence(
    graph: nx.DiGraph,
    a: set[str],
    b: set[str],
    e: set[str],
) -> bool:
    """
    Check if P(A | E, B) = P(A | E).
    :param graph: the Bayesian network
    :param a: node set A
    :param b: node set B
    :param e: the evidence set E
    """
    return is_d_separator(graph, a, b, e)


def search_max_independent_set(
    graph: nx.DiGraph,
    a: set[str],
    b: set[str],
    e: set[str],
) -> list[tuple[str, ...]]:
    """
    Given evidence E, node set A and B, find max subsets of B that's
    independent with A given E and subset complement of B.
    """
    def _predicate(sub_b):
        sub_b = set(sub_b)
        return check_conditional_independence(graph, a, sub_b, e | (b - sub_b))

    return utils.get_max_subsets(b, _predicate)
