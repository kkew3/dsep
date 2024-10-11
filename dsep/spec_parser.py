"""
Defines the graph spec parser.
"""

import dataclasses
import itertools

import pyparsing as pp
import networkx as nx
from networkx.algorithms import is_directed_acyclic_graph


def define_grammar():
    IDENTIFIER = pp.Word(pp.identchars, pp.identbodychars)
    EDGE_OP = pp.Literal('--') | '->'

    node_id = IDENTIFIER
    node_id_list = pp.Group(
        pp.OneOrMore(node_id + pp.Opt(pp.Suppress(pp.Literal(';') | ','))))
    subgraph = pp.Suppress('{') + node_id_list + pp.Suppress('}')
    edge_rhs = pp.Forward()
    edge_rhs << (EDGE_OP + (node_id | subgraph) + pp.ZeroOrMore(edge_rhs))
    edge_stmt = pp.Group((node_id | subgraph) + edge_rhs)
    edge_stmt_list = pp.ZeroOrMore(edge_stmt + pp.Opt(pp.Suppress(';')))
    return edge_stmt_list


GRAMMAR = define_grammar()


@dataclasses.dataclass
class EdgeGroup:
    """All edges from the underlying complete bipartite graph."""
    directed: bool
    nodes_a: list[str]
    nodes_b: list[str]


def parse_to_edge_groups(string: str) -> list[EdgeGroup]:
    r = GRAMMAR.parse_string(string, parse_all=True)
    edge_groups = []
    for stmt in r:
        iter_ = (stmt[i:i + 3] for i in range(0, len(stmt) - 2, 2))
        for nodes_a, edge_type, nodes_b in iter_:
            directed = True if edge_type == '->' else False
            nodes_a = [nodes_a] if isinstance(nodes_a, str) else list(nodes_a)
            nodes_b = [nodes_b] if isinstance(nodes_b, str) else list(nodes_b)
            edge_groups.append(EdgeGroup(directed, nodes_a, nodes_b))
    return edge_groups


class MixedEdgeTypesError(Exception):
    """Raised if directed and undirected edges are mixed in one graph."""
    pass


class DirectedCyclicError(Exception):
    """Raised if a directed graph is cyclic."""
    pass


def build_graph(edge_groups: list[EdgeGroup]) -> nx.Graph | nx.DiGraph:
    if all(e.directed for e in edge_groups):
        graph = nx.DiGraph()
    elif all(not e.directed for e in edge_groups):
        graph = nx.Graph()
    else:
        raise MixedEdgeTypesError
    for e in edge_groups:
        graph.add_edges_from(itertools.product(e.nodes_a, e.nodes_b))
    if isinstance(graph, nx.DiGraph):
        if not is_directed_acyclic_graph(graph):
            raise DirectedCyclicError
    return graph
