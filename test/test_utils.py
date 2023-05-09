import time

from termcolor import colored

from graph import Graph, Vertex, Edge
from graph_io import load_graph, write_dot


def format_groups(graphs, groups):
    graph_ids = assign_ids(graphs)
    for group in groups:
        group.graphs = [graph_ids[g] for g in group.graphs]
        group.graphs.sort()
    groups.sort(key=lambda g: g.graphs[0])
    return groups


def assign_ids(graphs):
    graph_ids = {}
    for i, graph in enumerate(graphs):
        graph_ids[graph] = i
    return graph_ids


def test(path, file_groups, expected=None):
    print('\nexec\tload\tfile')
    exec_time, load_time = 0, 0
    start_time = time.time()
    output = ''

    expected_map = {}
    if expected != None:
        for e in expected:
            f = e.split('\n')[0].replace(':', '')
            expected_map[f] = e

    for files, func, func_out in file_groups:
        for f in files:
            res = test_path(path + f, func)
            exec_time += res[0]
            load_time += res[1]

            if func_out != None:
                block = func_out(f, res[3], res[2])
                output += block + '\n'

            line = '{:.2f}s\t{:.2f}s\t{:20}'.format(res[0], res[1], f)

            if f in expected_map:
                success = colored('SUCCESS', 'green') \
                    if f in expected_map and block == expected_map[f] + '\n' \
                    else colored('FAILED', 'red')
                line += success

            print(line)

    print('\ntotal exec:\t%.2fs' % exec_time)
    print('total load:\t%.2fs' % load_time)
    print('total time:\t%.2fs\n' % (time.time() - start_time))
    return output


def test_path(path, func):
    with open(path) as f:

        # load graphs from the file
        start_time = time.time()
        is_list = path.endswith('.grl')
        graphs = load_graph(f, read_list=is_list)[0] \
            if is_list else load_graph(f)
        load_time = time.time() - start_time

        # execute function on graphs
        start_time = time.time()
        output = func(graphs)
        exec_time = time.time() - start_time
        return exec_time, load_time, output, graphs


def save_dot_by_path(i, graphs_path, output_path):
    with open(graphs_path) as f1:
        graphs = load_graph(f1, read_list=True)[0]
        with open(output_path, 'w') as f2:
            write_dot(graphs[i], f2)


def save_dot(graph, output_path):
    with open(output_path, 'w') as f:
        write_dot(graph, f)


def create_graph(v_count, e_indices):
    graph = Graph(False, v_count)
    vertices = graph.vertices
    for i in e_indices:
        edge = Edge(vertices[i[0]], vertices[i[1]])
        graph.add_edge(edge)
    return graph
