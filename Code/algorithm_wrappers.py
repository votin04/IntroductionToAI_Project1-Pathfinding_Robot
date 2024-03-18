from GBFS import *
from Dijkstra import *
from aStar import *
from map import *

import copy

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

# A wrapper for Dijkstra algorithm
class FindPathInDynamicMap_wrapper:
    name = ""

    def __init__(self, map : Map, algorithm_class) -> None:
        self.map = map
        self.algorithm_class = algorithm_class
        self.name = algorithm_class.name

    def find_path(self) -> list :
        static_map = copy.deepcopy(self.map)
        static_map = static_map.generator.extendObstacleBounds(static_map)

        path_finder = self.algorithm_class(static_map)
        self.path = path_finder.find_path()

        return self.path
    
    def find_cost(self) -> int:
        if self.path is not None and len(self.path) != 0:
            return len(self.path) - 1
        else:
            return 0
