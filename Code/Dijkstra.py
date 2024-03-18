from map import *
import numpy as np
import heapq


class Dijkstra:
    def __init__(self, graph: np.array):
        self.graph = graph

    def dijkstra(self, start, end):
        rows, cols = self.graph.shape
        dist = np.full((rows, cols), np.inf)
        dist[start] = 0

        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_node == end:
                break

            if current_node in visited:
                continue

            visited.add(current_node)

            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                cost = current_dist + 1  # Assuming each step cost is 1
                if cost < dist[neighbor]:
                    dist[neighbor] = cost
                    heapq.heappush(pq, (cost, neighbor))
        return self.reconstruct_path(start, end, dist)

    def get_neighbors(self, node):
        rows,cols = self.graph.shape
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dx,dy in directions:
            x, y = node[1] + dx, node[0] + dy  
            if 0 <= x < cols and 0 <= y < rows and self.graph[y][x] != 1:
                neighbors.append((y, x))

        return neighbors

    def reconstruct_path(self, start, end, dist):
        current = end
        path = []
        visited = set()  

        while current != start:
            path.append(current[::-1])
            visited.add(current)
            neighbors = self.get_neighbors(current)
            found_neighbor = False

            for neighbor in neighbors:
                if dist[neighbor] == dist[current] - 1 and neighbor not in visited:
                    current = neighbor
                    found_neighbor = True
                    break

            if not found_neighbor:
                print("Unable to find a valid neighbor for node:", current)
                return []

        path.append(start[::-1])
        path.reverse()
        return path
