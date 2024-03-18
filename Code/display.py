from map import *
from GBFS import *
from Dijkstra import *
from aStar import *

import os
import matplotlib.pyplot as plt
import numpy as np

# A wrapper for aStar algorithm
class aStar_wrapper:
    name = 'AStar'

    def __init__(self, map : Map) -> None:
        self.map = map
        self.name = 'AStar'

    def find_path(self) -> list :
        matrix = self.map.matrix
        src = self.map.map_info.points['start']
        des = self.map.map_info.points['end']
        points = self.map.map_info.points['passing_points']
        max_row, max_col = (self.map.map_info.map_limits['row_num'], self.map.map_info.map_limits['col_num'])

        path_finder = AStar(matrix, src, des, points)
        
        self.path = path_finder.findPickUp()

        if self.path is not None:
            for i in range(len(self.path)):
                self.path[i] = (self.path[i][1], self.path[i][0])

        return self.path

    def find_cost(self) -> int:
        if self.path is not None:
            return len(self.path) - 1
        else:
            return 0

# A wrapper for Dijkstra algorithm
class Dijkstra_wrapper:
    name = 'Dijkstra'

    def __init__(self, map : Map) -> None:
        self.map = map

    def find_path(self) -> list :
        dijkstra = Dijkstra(self.map.matrix)

        # Find a path
        src_y=self.map.map_info.points['start'][1]
        src_x=self.map.map_info.points['start'][0]
        src = (src_y,src_x)

        des_y=self.map.map_info.points['end'][1]
        des_x=self.map.map_info.points['end'][0]
        des= (des_y,des_x)

        self.path = dijkstra.dijkstra(src, des) 

        return self.path
    
    def find_cost(self) -> int:
        if self.path is not None and len(self.path) != 0:
            return len(self.path) - 1
        else:
            return 0

# A wrapper for GBFS algorithm
class GBFS_wrapper:
    name = 'GBFS'

    def __init__(self, map : Map) -> None:
        self.map = map

    def find_path(self) -> list :
        limits = (self.map.map_info.map_limits['col_num'], self.map.map_info.map_limits['row_num'])
        src = self.map.map_info.points['start']
        des = self.map.map_info.points['end']
        polygons = self.map.map_info.obstacles

        gbfs = GBFS(self.map.matrix, limits, src, des, polygons)

        result = gbfs.greedy_best_first_search()
        if (result is None):
            self.path = []
        else:
            self.path = result[0]
    
        return self.path

    def find_cost(self) -> int:
        if self.path is not None and len(self.path) != 0:
            return len(self.path) - 1
        else:
            return 0

# Class used to display 2D output
class Displayer:
    map = Map()

    def __init__(self, map : Map) -> None:
        # Copy map_info
        self.map.map_info = map.map_info

        # Create a new similar matrix without obstacles marked
        self.map.matrix = np.zeros((map.map_info.map_limits['row_num'], map.map_info.map_limits['col_num']), dtype=int)

        src = (map.map_info.points['start'][0], map.map_info.points['start'][1])
        des = (map.map_info.points['end'][0], map.map_info.points['end'][1])
        passing = map.map_info.points['passing_points']
        
        self.map.matrix[src[1]][src[0]] = 1
        self.map.matrix[des[1]][des[0]] = 1
        for point in passing:
            self.map.matrix[point[1]][point[0]] = 1

    def draw_shape(self, vertices):
        # Draw filled polygon with colormap
        polygon = plt.Polygon(vertices, closed=True, edgecolor='black')
        plt.gca().add_patch(polygon)

    def draw_path(self, ax, path):
        if path:
            shortest_path = np.array(path)
            ax.plot(shortest_path[:, 0], shortest_path[:, 1], 'go', markersize=5, alpha=1)

        start = self.map.map_info.points['start']        
        end = self.map.map_info.points['end']        

        # Mark start and end points with 'S' and 'G'
        plt.text(start[0], start[1], 'S', color='white', fontsize=12, ha='center', va='center')
        plt.text(end[0], end[1], 'G', color='white', fontsize=12, ha='center', va='center')

    def set_axis(self):
        # Set ticks and labels for x-axis and y-axis
        plt.xticks(range(self.map.matrix.shape[1]), range(0, self.map.matrix.shape[1]))
        plt.yticks(range(self.map.matrix.shape[0]), range(0, self.map.matrix.shape[0]))

    def draw_grid(self):
        plt.grid(which="both", color="black", linewidth=0.5, alpha=0.2)

    def draw(self, path, cost, name, output_folder):
        matplotlib.use('Agg')
        fig, ax = plt.subplots()

        ax.imshow(self.map.matrix, cmap='Accent', interpolation='nearest', origin='lower')

        # Draw path
        self.draw_path(ax, path)

        # Draw obstacles
        for obstacle in self.map.map_info.obstacles:
            self.draw_shape(obstacle)

        # Set x-axis and y-axis
        self.set_axis()

        # Draw grid
        self.draw_grid()

        plt.title(f"{name} - Cost: {cost}")

        # Save plot
        if os.path.exists(f"{output_folder}/") == False:
            os.makedirs(f"{output_folder}/")

        image_name = f"{output_folder}/{name}.png"
        plt.savefig(image_name)
        plt.close()

        return image_name  