from pathlib import Path

import pyAgrum as gum
import click


def read_spec(path_or_spec: str):
    return (Path(path_or_spec).read_text()
            if Path(path_or_spec).is_file() else path_or_spec)


@click.command(
    help=('Test conditional independence between '
          'NODE_A and NODE_B given EVIDENCE in a Bayesian Network or '
          'a Markov Random Field. Print "yes" if they are conditionally '
          'independent, "no" otherwise.'))
@click.option(
    '-g',
    '--graph-type',
    'graph_type',
    type=click.Choice(['bn', 'mrf']),
    required=True,
    help=('Type of graph to use: Bayesian Network (bn) or '
          'Markov Random Field (mrf).'),
)
@click.option(
    '-i',
    '--spec',
    'path_or_spec',
    metavar='PATH_OR_SPEC',
    required=True,
    help='Either a path to the graph spec, or the spec string.')
@click.option(
    '-a',
    'node_a',
    metavar='NODE_A',
    required=True,
    help='The node A to test conditional independence.')
@click.option(
    '-b',
    'node_b',
    metavar='NODE_B',
    required=True,
    help='The node B to test conditional independence.')
@click.option(
    '-e',
    'evidence',
    metavar='EVIDENCE',
    default='',
    help='The evidence nodes, separated by commas. Default to empty set.')
def app(graph_type, path_or_spec, node_a, node_b, evidence):
    spec = read_spec(path_or_spec)
    evidence = evidence.split(',') if evidence else []
    # Since we only need to test conditional independence, keeping the domain
    # size (the 2nd argument to `gum.fastBN` or `gum.fastMRF`) as default value
    # suffices.
    g = gum.fastBN(spec) if graph_type == 'bn' else gum.fastMRF(spec)
    if g.isIndependent(node_a, node_b, evidence):
        click.echo('yes')
    else:
        click.echo('no')
