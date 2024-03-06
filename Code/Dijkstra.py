# Library for INT_MAX
from map import *
import numpy as np
import heapq
from map import *
 


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
            path.append(current)
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
                raise ValueError("No valid neighbor found. Unable to reconstruct path.")

        path.append(start)
        path.reverse()
        return path


'''TESTING SECTION'''                  
map = Map()
map.create('input.txt')

dijkstra = Dijkstra(map.matrix)

src_y=map.map_info.points['start'][1]
src_x=map.map_info.points['start'][0]
src = (src_y,src_x)
des_y=map.map_info.points['end'][1]
des_x=map.map_info.points['end'][0]
des= (des_y,des_x)

path = dijkstra.dijkstra(src, des)
print("Result:",path)

# Display the matrix
matplotlib.use('Agg')
plt.imshow(map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

shortest_path = np.array(path)
plt.plot(shortest_path[:, 1], shortest_path[:, 0], 'r-', linewidth=2)

# Add colorbar for reference
plt.colorbar()
plt.title('Map Matrix')
plt.savefig("matplotlib.png")