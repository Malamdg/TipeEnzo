from src.GameEntities.Board import Board, Road


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

    def topological_sort_util(self, v, visited, stack):
        visited.add(v)
        for neighbor in self.vertices[v]:
            if neighbor not in visited:
                self.topological_sort_util(neighbor, visited, stack)
        stack.append(v)

    def topological_sort(self):
        visited = set()
        stack = []

        for vertex in list(self.vertices):
            if vertex not in visited:
                self.topological_sort_util(vertex, visited, stack)

        return stack[::-1]  # Return in reverse order

    def find_longest_path(self, start):
        # Step 1: Topological Sort
        topological_order = self.topological_sort()

        # Step 2: Initialize distances
        dist = {vertex: float('-inf') for vertex in self.vertices}
        dist[start] = 0

        # Step 3: Relax edges according to topological order
        for vertex in topological_order:
            if dist[vertex] != float('-inf'):
                for neighbor in self.vertices[vertex]:
                    if dist[neighbor] < dist[vertex] + self.edges[(vertex, neighbor)]:
                        dist[neighbor] = dist[vertex] + self.edges[(vertex, neighbor)]

        return dist


class UndirectedGraph(Graph):
    def __init__(self):
        super().__init__()

    def add_edge(self, start, end, weight=1):
        super().add_edge(start, end, weight)
        super().add_edge(end, start, weight)

    def init_from_road_list(self, roads: list[Road]):
        for road in roads:
            self.add_edge(road.start.value, road.end.value, road.length)

    def init_from_board(self, board: Board):
        self.init_from_road_list(board.roads)

    def is_connected(self, start, end):
        """
        Use DFS to check if there's a path between start and end.
        """
        visited = set()
        stack = [start]

        if start not in self.vertices.keys() or end not in self.vertices.keys():
            return False

        while stack:
            vertex = stack.pop()
            if vertex == end:
                return True
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(self.vertices[vertex] - visited)

        return False


class Algorithm:
    @staticmethod
    def longest_road(player):
        player_roads = player.roads
        graph = UndirectedGraph()
        graph.init_from_road_list(player_roads)

        longest_path_length = 0
        for vertice in graph.vertices:
            dist = graph.find_longest_path(vertice)
            longest_path_length = max(longest_path_length, max(dist.values()))

        return longest_path_length

    @staticmethod
    def update_objective_cards(player):
        graph = UndirectedGraph()
        graph.init_from_road_list(player.roads)
        for objective_card in player.objectives.cards:
            if Algorithm.is_complete(objective_card, graph):
                objective_card.set_completed()

    @staticmethod
    def is_complete(objective_card, graph):
        if objective_card is None:
            return False
        return graph.is_connected(objective_card.start.value, objective_card.destination.value)

