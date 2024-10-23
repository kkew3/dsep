# d-sep

Command line utility to test conditional independence in Bayesian network (BN) and Markov random field (MRF).
[`networkx`](https://networkx.org/) is used as backend to test d-separation in Bayesian networks.

## Installation

We recommend [`pipx`](https://github.com/pypa/pipx):

```bash
pipx install git+https://github.com/kkew3/dsep.git@master
```

Of course, you may also use `pip` directly, or clone this repo and run `pip install -e .`.

## Graph spec

`dsep` supports a subset features of [`graphviz`](https://graphviz.org/) language.
For examples, these are valid edge definitions for a Bayesian network:

```dot
A -> B;
A -> B -> C;
{A, B} -> {C, D} -> E;
```

`pyparsing` is used to parse the graph spec.

## Basic usage

See `dsep --help` for details.

Example:

```bash
dsep -i "X -> {A, B}" -a A -b B -e X
```

outputs:

```
yes
```

The node set A (`-a`), set B (`-b`) and evidence (`-e`) are not restricted to a single node.

## Other features

There's an option `-m` for BN.
It's a shortcut function that finds the max subsets of B that are independent with A given E and B's subset complement.

For example,

```bash
dsep -i '{a,b,c,d} -> e; d -> a' -a a -b 'b,c,d' -m
```

gives

```
(a) ⊥ (c,b) | (d)
```

## Test

Clone this repo, and run

```bash
pip install -e '.[dev]'
pytest
```

## Project state

WIP.

I've finished the BN part, but not for MRF.

See [TODO.md](./TODO.md) for details.

## License

MIT.
