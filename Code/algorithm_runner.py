from display import *
from algorithm_wrappers import *
from display_dynamic import *

'''Pass into this class a map class, list of algorithm classes that you want to run, displayer class used to draw output,
source test case folder and destination folder used to store all results'''
class AlgorithmRunner:
    def __init__(self, map_class,  algorithm_class, displayer_class, input_file, ouput_folder):
        self.map_class = map_class
        self.algorithm_class = algorithm_class
        self.displayer_class = displayer_class
        self.input_file = input_file
        self.output_folder = ouput_folder

    def run(self):
        # Check validity of input file
        if os.path.exists(self.input_file):
            if self.input_file.endswith(".txt"):
                # Create a map for this input
                map = self.map_class()
                map.create(self.input_file)

                # If input has passing points, we just run AStar, not any other algorithms
                if map.map_info.points['passing_points'] and self.algorithm_class != aStar_wrapper:
                    raise Exception('The program just runs A* algorithm for input having check points.')

                # Create a displayer for this input
                displayer = self.displayer_class(map)

                # Get name of the algorithm
                algorithm_name = self.algorithm_class.name

                # Print prompt
                print(f"Finding path with {algorithm_name} algorithm...")

                # Find path in dynamic map
                if self.displayer_class == Displayer_dynamic:
                    algorithm_instance = FindPathInDynamicMap_wrapper(map, self.algorithm_class)
                    path = algorithm_instance.find_path()
                    cost = algorithm_instance.find_cost()
                else:
                    # Find path in normal map
                    path, cost = self.run_algorithm(self.algorithm_class, map)

                result_name = os.path.basename(self.input_file)
                
                # Display
                output_path = displayer.draw(path, cost, f"{algorithm_name}_{result_name.removesuffix('.txt')}", self.output_folder)

                print(f"Output of {result_name} with {algorithm_name} algorithm has been saved to {output_path}.")
            else:
                print("Invalid input file format. The program just runs with text file.")
        else:
            print("File not found.")

    def run_algorithm(self, algorithm_class, map):
        # Run the algorithm
        algorithm_instance = algorithm_class(map)
        path = algorithm_instance.find_path()
        cost = algorithm_instance.find_cost()

        return path, cost