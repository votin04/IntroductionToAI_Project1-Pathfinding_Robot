from map_3D import *
from display import Dijkstra_wrapper, aStar_wrapper, GBFS_wrapper

import os
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

class Displayer_3D:
    map = Map_3D()

    def __init__(self, map: Map_3D) -> None:
        # Copy map_info
        self.map.map_info = map.map_info

        # Create a new similar matrix without obstacles marked
        self.map.matrix = np.zeros((map.map_info.map_limits['row_num'], map.map_info.map_limits['col_num']), dtype=int)
        self.cube = np.zeros((map.map_info.map_limits['row_num'], map.map_info.map_limits['col_num'], map.map_info.map_limits['height']), dtype=int)

        src = (map.map_info.points['start'][0], map.map_info.points['start'][1])
        des = (map.map_info.points['end'][0], map.map_info.points['end'][1])
        passing = map.map_info.points['passing_points']

        self.map.matrix[src[1]][src[0]] = 1
        self.map.matrix[des[1]][des[0]] = 1

        self.cube[0][src[1]][src[0]] = 1
        self.cube[0][des[1]][des[0]] = 1

        for point in passing:
            self.map.matrix[point[1]][point[0]] = 1
            self.cube[0][point[1]][point[0]] = 1

    def draw_shape_3D(self, fig):
        # Draw obstacles
        for obstacle in self.map.map_info.obstacles_3D:
            x, y, z = zip(*obstacle)

            # Connect consecutive vertices to draw the sides of the obstacle
            for i in range(len(x)):
                for j in range(i + 1, len(x)):
                    fig.add_trace(go.Scatter3d(
                        x=[x[i], x[(j) % len(x)]],  # Connect to the next vertex or wrap around to the first vertex
                        y=[y[i], y[(j) % len(y)]],
                        z=[z[i], z[(j) % len(z)]],
                        mode='lines',
                        line=dict(color='black', width=2)
                    ))

            # Fill the shape with color
            fig.add_trace(go.Mesh3d(
                x=x,
                y=y,
                z=z,
                color='orange',  # Adjust the color as needed
                opacity=1,
                alphahull=0  # Disable alpha hull to ensure solid fill
            ))

    def draw_path(self, fig, path):
        if path:
            shortest_path = np.array(path)
            x, y, z = shortest_path[:, 0], shortest_path[:, 1], np.zeros_like(shortest_path[:, 1])
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5, color='green', opacity=1)))

        start = self.map.map_info.points['start']
        end = self.map.map_info.points['end']

        # Mark start and end points with 'S' and 'G'
        fig.add_trace(go.Scatter3d(x=[start[0]], y=[start[1]], z=[0], mode='text', text='S', textposition='top center', textfont=dict(size=12, color='red')))
        fig.add_trace(go.Scatter3d(x=[end[0]], y=[end[1]], z=[0], mode='text', text='G', textposition='top center', textfont=dict(size=12, color='red')))

    def draw_3d(self, path, cost, name, output_folder):
        # Create a 3D scatter plot for the cube
        fig = go.Figure(data=[go.Scatter3d(x=[]*self.map.map_info.map_limits['col_num'],
                                        y=[]*self.map.map_info.map_limits['row_num'],
                                        z=[0]*self.map.map_info.map_limits['height'])])

        # Draw obstacles
        self.draw_shape_3D(fig)

        # Draw path
        self.draw_path(fig, path)

        # Set axis labels
        fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

        # Set the layout
        fig.update_layout(title=f"{name} - Cost: {cost}")

        # Save or show the plot
        if os.path.exists(f"{output_folder}/") == False:
            os.makedirs(f"{output_folder}")
        fig.write_html(f"{output_folder}/{name}.html")

class AlgorithmTester_3D:
    def __init__(self, algorithms, input_folder, output_folder):
        self.algorithms = algorithms
        self.input_folder = input_folder
        self.output_folder = output_folder

    def run_tests(self):
        for filename in os.listdir(self.input_folder):
            # Iterate through all inputs
            if filename.endswith(".txt"):
                file_path = os.path.join(self.input_folder, filename)

                # Create a map for this input
                map = Map_3D()
                map.create(file_path)
                
                # Create a displayer for this input
                displayer = Displayer_3D(map)

                # Find path with each iterated algorithm
                for algorithm_class in self.algorithms:
                    algorithm_name = algorithm_class.name
                    print(f"Running tests for {algorithm_name}...")

                    # Find path
                    path, cost = self.run_test(algorithm_class, map)

                    # Display
                    displayer.draw_3d(path, cost, f"{algorithm_name}_{filename.removesuffix('.txt')}", self.output_folder)

    def run_test(self, algorithm_class, map):
        # Run the algorithm
        algorithm_instance = algorithm_class(map)
        path = algorithm_instance.find_path()
        cost = algorithm_instance.find_cost()

        return path, cost
    
algorithms = [Dijkstra_wrapper]
tester = AlgorithmTester_3D(algorithms, './Test_cases_3D', './Results_3D')
tester.run_tests()