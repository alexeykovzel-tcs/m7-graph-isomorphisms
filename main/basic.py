from graph_io import load_graph
from graph_iso import GraphIso
from enum import Enum
import multiprocessing
import time


def basicAut(file_name, graphs):
    output = file_name + ':\n{:<30}#Aut:\n'.format('Graph:')
    graph_ids = assign_ids(graphs)
    for graph in graphs:
        pair = [graph, graph.deep_copy()]
        groups = GraphIso(pair).group(with_count=True)
        count = 0 if len(groups) == 0 else groups[0].count
        output += '{:<30}{}\n'.format(str(graph_ids[graph]) + ':', count)
    print(output)


def basicGI(file_name, graphs):
    groups = GraphIso(graphs).group()
    format_groups(graphs, groups)
    output = file_name + ':\nEquivalence classes:\n'
    for group in groups:
        output += '{}\n'.format(group.graphs)
    print(output)


def basicGIAut(file_name, graphs):
    groups = GraphIso(graphs).group(with_count=True)
    format_groups(graphs, groups)
    output = file_name + ':\n'
    output += '{:<30}#Aut:\n'.format('Equivalence classes:')
    for group in groups:
        output += '{:<30}{}\n'.format(str(group.graphs), group.count)
    print(output)


class Basic(Enum):
    GI = basicGI
    AUT = basicAut
    GIAUT = basicGIAut


def exec_file(args):
    name, consumer = args
    with open(name) as f:
        graphs = load_graph(f, read_list=True)[0]
        consumer(name, graphs)


def format_groups(graphs, groups):
    graph_ids = assign_ids(graphs)
    for group in groups:
        group.graphs = [graph_ids[g] for g in group.graphs]
        group.graphs.sort()
    groups.sort(key=lambda g: g.graphs[0])


def assign_ids(graphs):
    graph_ids = {}
    for i, graph in enumerate(graphs):
        graph_ids[graph] = i
    return graph_ids


def run(files):
    start_time = time.time()
    print()

    with multiprocessing.Pool() as pool:
        pool.map(exec_file, files)

    total_time = time.time() - start_time
    print('total time:\t%.2fs\n' % total_time)
