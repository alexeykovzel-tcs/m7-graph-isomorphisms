from color import ColorGroup
from graph import Graph


class GraphColors(object):
    """
    Usage of GraphColors class:
    colors = GraphColors([G1, G2, ...])

    colors.all                      colors for each vertex by graph
    colors.near                     neighboring colors for each vertex 
    colors.next                     next color to be assigned

    colors.refine()                 refines the coloring
    colors.reset()                  resets colors to the initial state
    colors.group()                  groups graphs with the same coloring
    colors.count()                  counts the number of repeating colors
    colors.assign(V, C)             assigns a color (C) to a vertex (V)
    colors.vertices_of(G, C)        returns a list of vertices with a given color
    colors.copy([G1, G2, ...])      returns a copy of the colors for the given graphs
    """

    def __init__(self, graphs: list[Graph]):
        self.graphs = graphs

    def __str__(self):
        output = ''
        for graph_id, graph in enumerate(self.all):
            output += '\nGraph {}:\n'.format(graph_id)
            for vertex, color in self.all[graph].items():
                output += 'Vertex {}: {}\n'.format(vertex.label, color)
        return output

    def vertices_of(self, graph, color):
        """
        Returns a list of vertices with a given color.
        """
        return [vertex for vertex in graph.vertices
                if self.all[graph][vertex] == color]

    def first_vertex_of(self, graph, color):
        """
        Returns the first vertex with a given color.
        """
        for vertex in graph.vertices:
            if self.all[graph][vertex] == color:
                return vertex

    def reset(self):
        """
        Resets to the initial state by setting colors by vertex degree 
        and resetting the neighboring colors.
        """
        self.all = {graph: {} for graph in self.graphs}
        self.near = {}
        self.next = 0
        self.__set_by_degree()
        self.__reset_near()
        return self

    def copy(self, graphs):
        """
        Returns a copy of the colors for the given graphs.
        """
        colors = GraphColors(graphs)
        colors.next = self.next
        colors.all = {graph: self.all[graph].copy() for graph in graphs}
        colors.near = {vertex: self.near[vertex].copy()
                       for graph in graphs
                       for vertex in graph.vertices}
        return colors

    def assign(self, vertex, color):
        """
        Assigns a color to a vertex and updates its neighbors.
        """
        self.all[vertex.graph][vertex] = color
        for neighbor in vertex.neighbours:
            near = self.near[neighbor]
            near[color] = near.get(color, 0) + 1

    def group(self):
        """
        Returns a list of graph groups that are possibly isomorphic
        (with a boolean value of whether the coloring is descrete).
        A set is included if the number of colors is the same for both graphs.
        e.g. [([G1, G2], {0: 2, 1: 2}, False), ([G3], {0: 3}, True)]
        """
        # group graphs with the same number of colors
        groups = []
        for graph, colors in self.count().items():
            new_group = True
            # check if such a group already exists
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
        """
        Counts the number of repeating colors.
        e.g. { 0: 3 } means that color '0' appeared 3 times
        """
        count = {}
        for graph, colors in self.all.items():
            graph_count = {}
            count[graph] = graph_count
            for color in colors.values():
                graph_count[color] = graph_count.get(color, 0) + 1
        return count

    def refine(self):
        """
        Executes color refinement algorithm by updating colors based on the uniqueness of 
        colors in vicinity. The algorithm repeats until there are no longer updates.
        """
        # set all vertices to be iterated for the 1-st cycle
        colors_to_update = set(
            colors[vertex] for graph, colors in self.all.items() for vertex in graph)
        updated_vertices = set()

        while True:
            # update colors of vertices with different
            # surrounding colors (color vicinity)
            color_vicinity = {}
            new_mapping = {}
            updated_vertices.clear()
            for graph, colors in self.all.items():
                for vertex in graph:
                    color = colors[vertex]
                    if color in colors_to_update:
                        if self.__update(vertex, color_vicinity, new_mapping):
                            updated_vertices.add(vertex)

            # finish if there are no updated vertices,
            if len(updated_vertices) == 0:
                break

            # update neighboring colors only of vertices that were updated in this cycle
            # and set their neighbors to be updated in the next cycle
            colors_to_update.clear()
            for vertex in updated_vertices:
                colors = self.all[vertex.graph]
                new_color = colors[vertex]
                for neighbor in vertex.neighbours:
                    near = self.near[neighbor]
                    near[new_color] = near.get(new_color, 0) + 1
                    colors_to_update.add(colors[neighbor])
        return self

    def __update(self, vertex, vicinity, new_mapping) -> bool:
        """
        Assigns a new color to the vertex if the colors in vicinity are 
        different for vertices of the same color.
        :return: whether the color has changed
        """
        near = self.near[vertex]
        colors = self.all[vertex.graph]
        color = colors[vertex]

        if color not in vicinity:
            vicinity[color] = near
            return False

        if vicinity[color] == near:
            return False

        if color in new_mapping:
            for new_color in new_mapping[color]:
                if vicinity[new_color] == near:
                    colors[vertex] = new_color
                    return True
            new_mapping[color].append(self.next)
        else:
            new_mapping[color] = [self.next]

        colors[vertex] = self.next
        vicinity[self.next] = near
        self.next += 1
        return True

    def __set_by_degree(self):
        """
        Assigns colors based on a vertex degree.
        (for each new degree, the color is incremented)
        """
        degrees = {}
        for graph in self.all:
            for vertex in graph.vertices:
                degree = len(vertex.incidence)
                if degree not in degrees:
                    degrees[degree] = self.next
                    self.next += 1
                self.all[graph][vertex] = degrees[degree]

    def __reset_near(self):
        """
        Counts the number of neighboring colors of all vertexes.
        e.g. { 2: 3 } means that vertex with color '2' has 3 neighbours
        """
        for graph in self.all:
            for vertex in graph:
                near = {}
                for neighbor in vertex.neighbours:
                    color = self.all[vertex.graph][neighbor]
                    near[color] = near.get(color, 0) + 1
                self.near[vertex] = near
