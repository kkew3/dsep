from dsep import spec_parser
from dsep import bn as m


class TestSearchMaxIndependentSet:
    def test_dsep3_1(self):
        g = spec_parser.build_graph(
            spec_parser.parse_to_edge_groups('{a, b} -> c'))
        assert m.search_max_independent_set(g, set('a'), set('b'),
                                            set()) == [tuple('b')]

    def test_dsep3_2(self):
        g = spec_parser.build_graph(
            spec_parser.parse_to_edge_groups('{a, b} -> c'))
        assert m.search_max_independent_set(g, set('a'), set('b'),
                                            set('c')) == [()]

    def test_case_1(self):
        spec = '''x1 -> m1; x2 -> m2; x3 -> m3; x4 -> m4; x5 -> m5;
        m1 -> y3; m2 -> {y3, y4}; m3 -> {y3, y4, y5}; m4 -> {y4, y5}; m5 -> y5;
        {y3, y4} -> a4; {y4, y5} -> a5;'''
        g = spec_parser.build_graph(spec_parser.parse_to_edge_groups(spec))
        assert m.search_max_independent_set(
            g, {'y5'}, {'a4', 'a5'},
            {'x1', 'x2', 'x3', 'x4', 'x5', 'y3', 'y4'}) == [('a4',)]
