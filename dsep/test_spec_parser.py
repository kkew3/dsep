import pytest

from dsep import spec_parser as m


class TestDefineGrammar:
    def test_basic_directed(self):
        edge_groups = m.parse_to_edge_groups('a -> b')
        assert edge_groups == [m.EdgeGroup(True, ['a'], ['b'])]

    def test_basic_undirected(self):
        edge_groups = m.parse_to_edge_groups('a -- b')
        assert edge_groups == [m.EdgeGroup(False, ['a'], ['b'])]

    def test_all(self):
        edge_groups = m.parse_to_edge_groups('''\
a -> b;
{c, d} -> e;
f -> {g, h};
{i, j} -> {k, l};
{m} -> n;
o -> p -> q;
r -> {s, t} -> {u, v, w};
x -- y -> z;
''')
        assert edge_groups == [
            m.EdgeGroup(True, ['a'], ['b']),
            m.EdgeGroup(True, ['c', 'd'], ['e']),
            m.EdgeGroup(True, ['f'], ['g', 'h']),
            m.EdgeGroup(True, ['i', 'j'], ['k', 'l']),
            m.EdgeGroup(True, ['m'], ['n']),
            m.EdgeGroup(True, ['o'], ['p']),
            m.EdgeGroup(True, ['p'], ['q']),
            m.EdgeGroup(True, ['r'], ['s', 't']),
            m.EdgeGroup(True, ['s', 't'], ['u', 'v', 'w']),
            m.EdgeGroup(False, ['x'], ['y']),
            m.EdgeGroup(True, ['y'], ['z']),
        ]


class TestBuildGraph:
    def test_directed_dag(self):
        with pytest.raises(m.DirectedCyclicError):
            m.build_graph(m.parse_to_edge_groups('a -> b -> a'))

    def test_undirected_dag(self):
        m.build_graph(m.parse_to_edge_groups('a -- b -- a'))

    def test_mixed_edge_types(self):
        with pytest.raises(m.MixedEdgeTypesError):
            m.build_graph(m.parse_to_edge_groups('a -> b -- c'))
