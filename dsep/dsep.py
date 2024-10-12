from pathlib import Path
import typing as ty

import networkx as nx
import click

from dsep import spec_parser
from dsep import bn


def read_spec(path_or_spec: str):
    return (Path(path_or_spec).read_text()
            if Path(path_or_spec).is_file() else path_or_spec)


def pprint_nodes(nodes: ty.Iterable[str]) -> str:
    return '(' + ','.join(nodes) + ')'


@click.command()
@click.option(
    '-i',
    '--spec',
    'path_or_spec',
    metavar='PATH_OR_SPEC',
    required=True,
    help='Either a path to the graph spec, or the spec string.')
@click.option(
    '-a',
    'nodes_a',
    metavar='NODES_A',
    required=True,
    help=('The node set A to test conditional independence, '
          'separated by commas. Must be nonempty.'))
@click.option(
    '-b',
    'nodes_b',
    metavar='NODES_B',
    required=True,
    help=('The node set B to test conditional independence, '
          'separated by commas. Must be nonempty.'))
@click.option(
    '-e',
    'evidence',
    metavar='EVIDENCE',
    default='',
    help='The evidence nodes, separated by commas. Default to empty set.')
@click.option(
    '-m',
    '--find-max-b-subset',
    'max_subset',
    is_flag=True,
    default=False,
    help='Print max independent subsets of NODES_B with NODES_A instead.',
)
def app(
    path_or_spec: str,
    nodes_a: str,
    nodes_b: str,
    evidence: str,
    max_subset: bool,
):
    """
    Test conditional independence between  NODE_A and NODE_B given EVIDENCE
    in a Bayesian Network or a Markov Random Field. Print "yes" if they are
    conditionally independent, "no" otherwise.
    """
    assert nodes_a and nodes_b
    nodes_a = set(nodes_a.split(','))
    nodes_b = set(nodes_b.split(','))
    evidence = set(evidence.split(',') if evidence else [])
    spec = read_spec(path_or_spec)

    graph = spec_parser.build_graph(spec_parser.parse_to_edge_groups(spec))
    if isinstance(graph, nx.DiGraph):
        if not max_subset:
            if bn.check_conditional_independence(graph, nodes_a, nodes_b,
                                                 evidence):
                click.echo('yes')
            else:
                click.echo('no')
        else:
            for sub_b in bn.search_max_independent_set(graph, nodes_a, nodes_b,
                                                       evidence):
                aug_evi = sorted(evidence | (nodes_b - set(sub_b)))
                click.echo('{} ⊥ {} | {}'.format(
                    pprint_nodes(nodes_a), pprint_nodes(sub_b),
                    pprint_nodes(aug_evi)))
    else:
        raise NotImplementedError('MRF graph separation not implemented yet')
