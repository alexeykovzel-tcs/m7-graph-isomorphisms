from collections import deque
from color import Color, ColorGroup
from graph import Graph


class GraphFastRef:
    """
    Usage of GraphFastRefinement class:
    fastRef = GraphFastRefinement([G1, G2, ...])
    fastRef.initial_colouring()      defines the base colouring: uniform with a second colour with the vertices of smallest degree
    fastRef.refine()                 refines until queue is empty (that is graph is stable)
    """

    def __init__(self, graphs: set[Graph]):
        self.graphs = graphs
        self.queue = deque([])

    def reset(self):
        self.colors = {}
        self.labels = {}
        self.next = 0
        self.neighbours = {}

        # uniform colouring
        base_color = Color(self.next)
        self.colors[self.next] = base_color
        self.queue.append(base_color)
        for graph in self.graphs:
            for vertex in graph.vertices:
                self.labels[vertex] = self.next
                self.neighbours[vertex] = {}
                self.neighbours[vertex][self.next] = vertex.degree
                self.colors[self.next].states.append(vertex)
        self.next += 1

        return self

    def refine(self):
        while len(self.queue) != 0:
            self.refine_color()
        return self

    def refine_color(self):
        color = self.queue.popleft()
        color.inQueue = False
        neighbours = {}

        for i in range(len(color)):
            for n in color.states[i].neighbours:
                tuple = (self.labels[n], self.neighbours[n][color.label])
                if tuple not in neighbours:
                    neighbours[tuple] = set(())
                neighbours[tuple].add(n)

        for n in neighbours:
            color = n[0]

            if len(neighbours[n]) < len(self.colors[color]):
                new_color = Color(self.next)
                self.colors[new_color.label] = new_color
                self.next += 1

                j = len(self.colors[color]) - len(neighbours[n])
                if j > len(neighbours[n]) or self.colors[color].inQueue:
                    self.queue.append(new_color)
                    new_color.inQueue = True
                else:
                    self.queue.append(self.colors[color])
                    self.colors[color].inQueue = True

                for nn in neighbours[n]:
                    for neighbour in nn.neighbours:
                        if new_color.label not in self.neighbours[neighbour].keys():
                            self.neighbours[neighbour][new_color.label] = 0
                        self.neighbours[neighbour][new_color.label] += 1
                    self.colors[color].states.remove(nn)
                    self.colors[new_color.label].states.append(nn)
                    self.labels[nn] = new_color.label 

    def group(self):
        groups = []
        for graph, colors in self.count().items():
            # check if such group already exists
            new_group = True
            for group in groups:
                if group.colors == colors:
                    group.graphs.append(graph)
                    new_group = False
                    break
            # if not, create a new group
            if new_group:
                discrete = all(count == 1 for count in colors.values())
                groups.append(ColorGroup([graph], colors, discrete))

        # filter out groups with only one graph
        return [group for group in groups if len(group.graphs) > 1]

    def count(self) -> list[tuple[int, dict[int: int]]]:
        count = {}
        for color in self.colors.values():
            for vertex in color.states:
                graph = vertex.graph
                if graph not in count:
                    count[graph] = {}
                old_count = count[graph].get(color.label, 0)
                count[graph][color.label] = old_count + 1
        return count

    def vertices_of(self, graph, color):
        return [v for v in self.colors[color].states if v.graph is graph]

    def first_vertex_of(self, graph, color):
        for v in self.colors[color].states:
            if v.graph is graph:
                return v

    def copy(self, graphs: set[Graph]):
        copy = GraphFastRef(graphs)
        copy.colors = {c.label: c.copy(graphs) for c in self.colors.values()}
        copy.labels = {v: c for v, c in self.labels.items() if v.graph in graphs}
        copy.neighbours = {v: n.copy() for v, n in self.neighbours.items()}
        copy.next = self.next
        return copy

    def assign(self, vertex, color):
        if color not in self.colors:
            self.colors[color] = Color(color)

        for neighbour in vertex.neighbours:
            if color not in self.neighbours[neighbour].keys():
                self.neighbours[neighbour][color] = 0
            self.neighbours[neighbour][color] += 1

        self.colors[self.labels[vertex]].states.remove(vertex)
        self.colors[color].states.append(vertex)
        self.labels[vertex] = color