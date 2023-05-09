import sys, os

# appends the system path to the graph files
sys.path.append(os.path.abspath('main'))
sys.path.append(os.path.abspath('test'))

from color_ref_fast import GraphFastRef
from test_utils import test, format_groups


expected_path = 'test/color-ref-basic/test_expected.txt'
output_path = 'test/color-ref-basic/test_actual.txt'
samples_path = 'test/color-ref-basic/samples/'


def color_ref_out(f, graphs, groups):
    format_groups(graphs, groups)
    output = f + '\n'
    for group in groups:
        output += str(group.graphs)
        output += ' discrete\n' if group.discrete else '\n'
    return output


def color_ref(graphs):
    return GraphFastRef(graphs).reset().refine().group()


if __name__ == '__main__':
    f = open(expected_path, "r")
    expected = f.read().split('\n\n')[1:]
    out = 'Sets of possibly isomorphic graphs:\n\n'
    out += test(samples_path, [([
        'CrefBenchmark1.grl',
        'CrefBenchmark2.grl',
        'CrefBenchmark3.grl',
        'CrefBenchmark4.grl',
        'CrefBenchmark5.grl',
        'CrefBenchmark6.grl',
    ], 
        color_ref,
        color_ref_out
    )], expected)

    with open(output_path, 'w') as f:
        f.write(out)
