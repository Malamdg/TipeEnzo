from src.GameEntities.Board import Board


class Algorithm:
    pass


class Graph:
    def __init__(self):
        self.nodes = []
        self.arcs = {}

    def init_from_board(self, board: Board):
        for road in board.roads:
            start = road.start.value
            end = road.end.value
            if start not in self.nodes:
                self.nodes.append(start)
                self.arcs[start] = [end]

            if end not in self.nodes:
                self.nodes.append(end)
                self.arcs[end] = [start]

            if end in self.arcs[start] and start in self.arcs[end]:
                continue

            if end not in self.arcs[start]:
                self.arcs[start].append(end)

            if start not in self.arcs[end]:
                self.arcs[end].append(start)
