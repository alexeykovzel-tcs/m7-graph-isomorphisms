from collections import deque
from graph import Graph


class Color(object):
    def __init__(self, label):
        self.label = label
        self.inQueue = False
        self.states = deque()

    def __len__(self):
        return len(self.states)

    def __str__(self):
        return str(self.label)

    def copy(self, graphs: set[Graph]):
        copy = Color(self.label)
        copy.inQueue = self.inQueue
        copy.states = deque(v for v in self.states if v.graph in graphs)
        return copy
    
class ColorGroup(object):
    def __init__(self, graphs, colors, discrete):
        self.graphs = graphs
        self.colors = colors
        self.discrete = discrete