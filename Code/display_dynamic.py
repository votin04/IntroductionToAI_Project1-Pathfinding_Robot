# # '''TESTING SECTION'''                  
# static_map = Map() # Map to search path
# dynamic_map = Map() # Map to display the vibrancy of each obstacles

# static_map.create("test1.txt")
# static_map.matrix = static_map.generator.extendObstacleBounds(static_map).matrix
# dynamic_map.create("test1.txt")

# directions = [(1,0), (0,-1), (-1,0), (0,1) ]


# src = static_map.map_info.points['start']
# des = static_map.map_info.points['end']
# points = static_map.map_info.points['passing_points']


# searchPath = AStar(static_map.matrix, src, des, points)

# src = searchPath.reverse_tuple(static_map.map_info.points['start'])
# des = searchPath.reverse_tuple(static_map.map_info.points['end'])

# baseline_path = searchPath.aStar(src, des)

# # Display the static matrix
# matplotlib.use('Agg')
# plt.imshow(static_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
# # Add colorbar for reference
# plt.title('Map Matrix')
# plt.savefig("static_map.png")

# renderPath = []

# for step in baseline_path:
#     for dx, dy in directions:
#         obstacles = dynamic_map.map_info.update_obstacles(dx, dy)
#         dynamic_map.createWithNewObstacles(obstacles)

#         renderPath.append(step)
#         path = np.array(renderPath)
#         plt.plot(path[:, 1], path[:, 0], 'go', markersize=5, alpha=1)

#         # Display the dynamic matrix
#         matplotlib.use('Agg')
#         plt.imshow(dynamic_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

#         # Add colorbar for reference
#         plt.title('Map Matrix')
#         plt.savefig("dynamic_map.png")
#         time.sleep(0)

    
import os
import time
from map import *
from display import Displayer
import imageio

'''Class used to display dynamic output'''
class Displayer_dynamic:
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

    def draw(self, path, cost, name, output_folder):
        displayer = Displayer(self.map)

        directions = [(1,0), (0,-1), (-1,0), (0,1)]
        renderPath = []
        images = []

        cnt = 0
        for step in path:
            cnt += 1
            for dx, dy in directions:
                obstacles = self.map.map_info.update_obstacles(dx, dy)
                self.map.createWithNewObstacles(obstacles)

                renderPath.append(step)
                image = displayer.draw(renderPath, cnt, " ", "Results_dynamic")

                images.append(imageio.v2.imread(image))    

        if os.path.exists(f"{output_folder}/") == False:
            os.makedirs(f"{output_folder}/")

        video_name = f"{output_folder}/{name}_dynamic.gif"

        imageio.v2.mimsave(video_name, images, duration=500)
        
        os.remove(image)