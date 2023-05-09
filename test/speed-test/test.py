import sys,os

# appends the system path to the graph files
sys.path.append(os.path.abspath('main'))
sys.path.append(os.path.abspath('test'))

from graph import Graph
from test_utils import test, format_groups
from graph_iso import GraphIso


samples_path = 'test/speed-test/samples/'
expected_path = 'test/speed-test/test_expected.txt'
out_path = 'test/speed-test/test_actual.txt'


def basicAut(graph: Graph):
    iso = GraphIso([graph, graph.deep_copy()])
    iso_groups = iso.group(with_count=True)
    return 0 if len(iso_groups) == 0 else iso_groups[0].count


def basicAut_out(f, graphs, count):
    output = f + ':\nGraph:\t\t#Aut:\n'
    output += '0\t\t\t' + str(count) + '\n'
    return output


def basicGI(graphs: list[Graph]):
    return GraphIso(graphs).group()


def basicGI_out(f, graphs, iso_groups):
    format_groups(graphs, iso_groups)
    output = f + ':\nEquivalence classes:\n'
    for group in iso_groups:
        output += '{}\n'.format(group.graphs)
    return output


def basicGIAut(graphs: list[Graph]):
    return GraphIso(graphs).group(with_count=True)


def basicGIAut_out(f, graphs, iso_groups):
    format_groups(graphs, iso_groups)
    out = f + ':\n'
    out += 'Equivalence classes:\t\t#Aut:\n'
    for group in iso_groups:
        out += '{}\t\t\t\t{}\n'.format(group.graphs, group.count)
    return out


if __name__ == '__main__':
    f = open(expected_path, "r")
    expected = f.read().split('\n\n')[1:]

    out = test(samples_path, [
        (['basicAut1.gr', 'basicAut2.gr'], basicAut, basicAut_out),
        (['basicGI1.grl', 'basicGI2.grl', 'basicGI3.grl'], basicGI, basicGI_out),
        (['basicGIAut1.grl'], basicGIAut, basicGIAut_out),
    ], expected)

    with open(out_path, 'w') as f:
        f.write('Speed test:\n\n' + out)