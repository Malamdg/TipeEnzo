from src.GameEntities.Board import Board, Road
from src.Players import Player


class Algorithm:
    @staticmethod
    def player_longest_road(player: Player, board: Board):
        player_roads = board.get_roads_by_player()[player.color]
        graph = UndirectedGraph()
        graph.init_from_road_list(player_roads)


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = set()

    def add_edge(self, start, end, weight=1):
        self.add_vertice(start)
        self.add_vertice(end)
        self.vertices[start].add(end)
        self.edges[(start, end)] = weight


class UndirectedGraph(Graph):
    def __init__(self):
        super().__init__()

    def add_edge(self, start, end, weight=1):
        super().add_edge(start, end, weight)
        super().add_edge(end, start, weight)

    def init_from_road_list(self, roads: list[Road]):
        for road in roads:
            self.add_edge(road.start, road.end, road.length)

    def init_from_board(self, board: Board):
        self.init_from_road_list(board.roads)
