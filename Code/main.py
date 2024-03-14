import time
import os
from map import *
from aStar import *

# '''TESTING SECTION'''                  
map = Map()
map.create("Test_cases/test1.txt")

directions = [(1,0), (0,-1), (-1,0), (0,1) ]

searchPath = AStar(map.matrix, map.map_info.points['start'], map.map_info.points['start'], map.map_info.points['passing_points'])
src = searchPath.reverse_tuple(map.map_info.points['start'])
des = searchPath.reverse_tuple(map.map_info.points['end'])

baseline_path = searchPath.aStar(src, des)

print(baseline_path)

while True:
    for dx, dy in directions:
        obstacles = map.map_info.update_obstacle(dx, dy)
        map.createWithNewObstacles(obstacles)
        # Display the matrix
        matplotlib.use('Agg')
        plt.imshow(map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
        # Add colorbar for reference
        plt.title('Map Matrix')
        plt.savefig("map.png")
        time.sleep(0)

    

