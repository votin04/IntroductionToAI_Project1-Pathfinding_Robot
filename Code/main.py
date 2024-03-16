# import time
# import os
# from map import *
# from aStar import *
# from display import Displayer

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
from aStar import *
from display import Displayer
import imageio

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
for i, tup in enumerate(baseline_path):
    baseline_path[i] = searchPath.reverse_tuple(tup)

# Display the static matrix
matplotlib.use('Agg')
plt.imshow(static_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
# Add colorbar for reference
plt.title('Map Matrix')

if os.path.exists('Results_vibrancy/') == False:
    os.makedirs("Results_vibrancy/")

plt.savefig("Results_vibrancy/static_map.png")
plt.close()

renderPath = []
displayer = Displayer(dynamic_map)

images = []

cnt = 0
for step in baseline_path:
    cnt += 1
    for dx, dy in directions:
        obstacles = dynamic_map.map_info.update_obstacles(dx, dy)
        dynamic_map.createWithNewObstacles(obstacles)

        renderPath.append(step)
        # path = np.array(renderPath)
        # plt.plot(path[:, ], path[:, 0], 'go', markersize=5, alpha=1)

        # # Display the dynamic matrix
        # matplotlib.use('Agg')
        # plt.imshow(dynamic_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

        # # Add colorbar for reference
        # plt.title('Map Matrix')
        # plt.savefig("dynamic_map.png")
        images.append(imageio.v2.imread(displayer.draw(renderPath, cnt - 1, f"dynamic_map", "Results_Vibrancy")))
        time.sleep(0)

imageio.v2.mimsave('Results_Vibrancy/video.gif', images, duration=500)