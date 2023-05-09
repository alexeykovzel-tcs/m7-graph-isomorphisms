import sys, os

# appends the system path to the graph files
sys.path.append(os.path.abspath('main'))
sys.path.append(os.path.abspath('test'))

from test_utils import format_groups, test
from graph_iso import GraphIso
from graph import Graph


expected_path = 'test/branching/test_expected.txt'
output_path = 'test/branching/test_actual.txt'
samples_path = 'test/branching/samples/'
graph_files = [
    # 'torus24.grl',
    # 'torus72.grl',
    # 'torus144.grl',
    # 'products72.grl',
    # 'products216.grl',
    # 'cographs1.grl',
    # 'trees11.grl',
    # 'trees36.grl',
    # 'trees90.grl',
    'modulesC.grl',
    # 'modulesD.grl',
    # 'cubes3.grl',
    # 'cubes5.grl',
    # 'cubes6.grl',
    # 'cubes7.grl',
    # 'cubes9.grl',
    # 'bigtrees1.grl',
    # 'bigtrees2.grl',
    # 'bigtrees3.grl',
    # 'wheeljoin14.grl',
    # 'wheeljoin33.grl',
    # 'wheelstar12.grl',
    # 'wheelstar15.grl',
]


def iso_groups_out(f, graphs, groups):
    format_groups(graphs, groups)
    output = f + ':\n'
    for group in groups:
        output += '{} {}\n'.format(str(group.graphs), str(group.count))
    return output

def iso_groups(graphs: set[Graph]):
    return GraphIso(graphs).group(with_count=True)


if __name__ == "__main__":
    f = open(expected_path, "r")
    expected = f.read().split('\n\n')[1:]

    out = 'Isomorphic pairs:\n\n'
    out += test(samples_path, [(
        graph_files, 
        iso_groups,
        iso_groups_out
    )], expected)

    with open(output_path, 'w') as f:
        f.write(out)
