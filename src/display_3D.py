from map_3D import *

import os
import numpy as np
import plotly.graph_objects as go

'''Class used to display 3D output'''
class Displayer_3D:
    map = Map_3D()

    def __init__(self, map: Map_3D) -> None:
        # Copy map_info
        self.map.map_info = map.map_info

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

        # List to store start, end and passing points to mark them with another color later
        special_points = []

        start = self.map.map_info.points['start']
        end = self.map.map_info.points['end']

        special_points.append(start)
        special_points.append(end)

        # Mark start and end points with 'S' and 'G'
        fig.add_trace(go.Scatter3d(x=[start[0]], y=[start[1]], z=[0], mode='text', text='S', textposition='top center', textfont=dict(size=12, color='red')))
        fig.add_trace(go.Scatter3d(x=[end[0]], y=[end[1]], z=[0], mode='text', text='G', textposition='top center', textfont=dict(size=12, color='red')))

        # Mark passing points with 'Check point' if any
        for point in self.map.map_info.points['passing_points']:
            special_points.append(point)
            fig.add_trace(go.Scatter3d(x=[point[0]], y=[point[1]], z=[0], mode='text', text='Check point', textposition='top center', textfont=dict(size=12, color='blue')))
        
        # Color special points
        for point in special_points:
            fig.add_trace(go.Scatter3d(x=[point[0]], y=[point[1]], z=[0], mode='markers', marker=dict(size=5, color='blue', opacity=1)))
        
        

    def draw(self, path, cost, name, output_folder):
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

        result_path = f"{output_folder}/{name}.html"
        fig.write_html(result_path)

        return result_path  