from map import *
from GBFS import *
from Dijkstra import *
from aStar import *

import os
import matplotlib.pyplot as plt
import copy

# A wrapper for aStar algorithm
class aStar_wrapper:
    name = 'AStar'

    def __init__(self, map : Map) -> None:
        self.map = map
        self.name = 'AStar'

    def find_path(self) -> list :
        src = []
        des = []
        src.append(self.map.map_info.points['start'][1])
        src.append(self.map.map_info.points['start'][0])
        des.append(self.map.map_info.points['end'][1])
        des.append(self.map.map_info.points['end'][0])

        points = self.map.map_info.points['passing_points']

        searchPath = AStar(self.map.matrix, src, des, points)
        
        src = searchPath.reverse_tuple(src)
        des = searchPath.reverse_tuple(des)
        
        self.path = searchPath.aStar(src, des)

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
        if self.path is not None:
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
        if self.path is not None:
            return len(self.path) - 1
        else:
            return 0

class Displayer:
    @staticmethod
    def draw(matrix, path, cost, name):
        matplotlib.use('Agg')
        plt.imshow(matrix, cmap='viridis', interpolation='nearest', origin='lower')

        if path:
            shortest_path = np.array(path)
            plt.plot(shortest_path[:, 0], shortest_path[:, 1], 'go', markersize=5, alpha=0.5)

        plt.colorbar()
        plt.title(name)
        plt.savefig(f"Results/{name}.png")
        plt.close()

class AlgorithmTester:
    def __init__(self, algorithms, map_folder='./Test_cases'):
        self.algorithms = algorithms
        self.map_folder = map_folder

    def run_tests(self):
        for filename in os.listdir(self.map_folder):
            # Iterate through all inputs
            if filename.endswith(".txt"):
                file_path = os.path.join(self.map_folder, filename)

                # Create a map for this input
                map = Map()
                map.create(file_path)

                # Find path with each iterated algorithm
                for algorithm_class in self.algorithms:
                    map_copy = copy.deepcopy(map)

                    algorithm_name = algorithm_class.name
                    print(f"Running tests for {algorithm_name}...")

                    path, cost = self.run_test(algorithm_class, map_copy)

                    Displayer.draw(map_copy.matrix, path, cost, f"{algorithm_name}_{filename.removesuffix('.txt')}")


    def run_test(self, algorithm_class, map):
        # Run the algorithm
        algorithm_instance = algorithm_class(map)
        path = algorithm_instance.find_path()
        cost = algorithm_instance.find_cost()

        return path, cost
    

algorithms = [aStar_wrapper, Dijkstra_wrapper, GBFS_wrapper]
tester = AlgorithmTester(algorithms)
tester.run_tests()