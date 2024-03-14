import time
import os
from map import *
from aStar import *
from display import Displayer

# '''TESTING SECTION'''                  
static_map = Map() # Map to search path
dynamic_map = Map() # Map to display the vibrancy of each obstacles

static_map.create("test1.txt")
static_map.matrix = static_map.generator.extendObstacleBounds(static_map).matrix
dynamic_map.create("test1.txt")

directions = [(1,0), (0,-1), (-1,0), (0,1) ]


src = static_map.map_info.points['start']
des = static_map.map_info.points['end']
points = static_map.map_info.points['passing_points']


searchPath = AStar(static_map.matrix, src, des, points)

src = searchPath.reverse_tuple(static_map.map_info.points['start'])
des = searchPath.reverse_tuple(static_map.map_info.points['end'])

baseline_path = searchPath.aStar(src, des)

print(baseline_path)

# Display the static matrix
matplotlib.use('Agg')
plt.imshow(static_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
# Add colorbar for reference
plt.title('Map Matrix')
plt.savefig("static_map.png")

while True:
    for dx, dy in directions:
        obstacles = dynamic_map.map_info.update_obstacles(dx, dy)
        dynamic_map.createWithNewObstacles(obstacles)
        # Display the dynamic matrix
        matplotlib.use('Agg')
        plt.imshow(dynamic_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
        # Add colorbar for reference
        plt.title('Map Matrix')
        plt.savefig("dynamic_map.png")
        time.sleep(0)

    

