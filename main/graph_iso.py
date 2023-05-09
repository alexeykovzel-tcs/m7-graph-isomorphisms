from color_ref_fast import GraphFastRef
from color_ref import GraphColors
from graph import Graph
import sys


detect_forests = True
detect_false_twins = True
use_fast_refinement = True


class IsoGroup:
    def __init__(self, graphs: set[Graph], count=0):
        self.graphs = graphs
        self.count = count


class GraphIso:
    def __init__(self, graphs: set[Graph]):
        self.graphs = graphs

        # detect graph forests
        if detect_forests:
            self.forests = set(g for g in graphs if g.is_forest())

        # detect false twins
        if detect_false_twins:
            self.false_twins = self.__false_twins()

    def group(self, with_count=False):
        grouped_graphs = set()
        groups = []

        # find all isomorphic groups
        colorRef = GraphFastRef(self.graphs) \
            if use_fast_refinement else GraphColors(self.graphs)
        colors = colorRef.reset().refine()
        for color_group in colors.group():
            graphs = color_group.graphs
            for i in range(len(graphs) - 1):
                if graphs[i] in grouped_graphs:
                    continue

                # create a new isomorphic group
                group = IsoGroup({graphs[i]})
                groups.append(group)
                for j in range(i + 1, len(graphs)):
                    pair = [graphs[i], graphs[j]]
                    main_branch = colors.copy(pair)

                    # check if graphs are isomorphic
                    isomorphic = False
                    if with_count and group.count == 0:
                        count = self.__count(pair, main_branch)
                        if count > 0:
                            group.count = count
                            isomorphic = True
                    else:
                        count = self.__count(pair, main_branch, only_one=True)
                        isomorphic = count == 1

                    if isomorphic:
                        group.graphs.add(graphs[j])
                        grouped_graphs.add(graphs[j])
        
        # handle signle graph groups
        for group in groups:
            if len(group.graphs) == 1 and group.count == 0:
                graph = list(group.graphs)[0]
                pair = [graph, graph.deep_copy()]
                new_count = GraphIso(pair).group(with_count=True)[0].count
                group.count = new_count

        return groups

    def __count(self, graphs, colors, only_one=False):
        color_groups = colors.group()
        total_count = 0

        # if coloring is unbalanced, there are no isomorphisms
        if len(color_groups) == 0:
            return 0

        # if coloring defines a bijection, there is only 1 automorphism
        if color_groups[0].discrete:
            return 1

        # branching rules: choosing the color class
        color_set = color_groups[0].colors
        branch_color = min(color_set, key=lambda c: color_set[c] if color_set[c] > 1 else sys.maxsize)

        # get x and y vertices
        y_all = colors.vertices_of(graphs[1], branch_color)
        x = colors.first_vertex_of(graphs[0], branch_color)

        # count isomorphisms for each possible branch
        y_precounted = {}
        for y in y_all:
            if y in y_precounted:
                total_count += y_precounted[y]
                continue

            # calculate isomorphisms for this branch
            branch = colors.copy(graphs)
            branch.assign(x, branch.next)
            branch.assign(y, branch.next)

            if use_fast_refinement:
                next_color = branch.colors[branch.next]
                branch.queue.append(next_color)

            branch.next += 1
            branch.refine()

            # calculate isomorphisms for this branch
            count = self.__count(graphs, branch, only_one)
            if only_one and count == 1:
                return 1

            # copy results for forests
            if detect_forests and graphs[0] in self.forests:
                y_precounted = {v: count for v in y_all}

            # copy results for false twins
            if detect_false_twins:
                for vertex in self.false_twins[y]:
                    y_precounted[vertex] = count

            total_count += count

        return total_count

    def __false_twins(self):
        false_twins = {}
        for graph in self.graphs:
            for v1 in graph.vertices:
                false_twins[v1] = set()
                for v2 in graph.vertices:

                    n1 = set(v1._incidence.keys())
                    n2 = set(v2._incidence.keys())

                    if v1 != v2 and n1 == n2 and not v1.is_adjacent(v2):
                        false_twins[v1].add(v2)

        return false_twins
