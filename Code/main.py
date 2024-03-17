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

    
# import os
# import time
# from map import *
# from aStar import *
# from display import Displayer
# import imageio

# '''TESTING SECTION'''                  
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
# for i, tup in enumerate(baseline_path):
#     baseline_path[i] = searchPath.reverse_tuple(tup)

# Display the static matrix
# matplotlib.use('Agg')
# plt.imshow(static_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
# Add colorbar for reference
# plt.title('Map Matrix')

# if os.path.exists('Results_vibrancy/') == False:
#     os.makedirs("Results_vibrancy/")

# plt.savefig("Results_vibrancy/static_map.png")
# plt.close()

# renderPath = []
# displayer = Displayer(dynamic_map)

# images = []

# cnt = 0
# for step in baseline_path:
#     cnt += 1
#     for dx, dy in directions:
#         obstacles = dynamic_map.map_info.update_obstacles(dx, dy)
#         dynamic_map.createWithNewObstacles(obstacles)

#         renderPath.append(step)
#         path = np.array(renderPath)
#         plt.plot(path[:, ], path[:, 0], 'go', markersize=5, alpha=1)

#         # Display the dynamic matrix
#         matplotlib.use('Agg')
#         plt.imshow(dynamic_map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

#         # Add colorbar for reference
#         plt.title('Map Matrix')
#         plt.savefig("dynamic_map.png")
#         images.append(imageio.v2.imread(displayer.draw(renderPath, cnt - 1, f"dynamic_map", "Results_Vibrancy")))
#         time.sleep(0)

# imageio.v2.mimsave('Results_Vibrancy/video.gif', images, duration=500)


import argparse
import os
import time
from map import *
from AStar import *
from display import Displayer
import imageio

def main():
    parser = argparse.ArgumentParser(description="Pathfinding Robot")

    #parser.add_argument("-filename", required=True)
    parser.add_argument("-level", type=int, required=True)
    parser.add_argument("-mode", choices=["3D", "2D"], required=True)
    parser.add_argument("-search", choices=["dijkstra", "astar", "gbfs","dynamic"], required=True)

    args = parser.parse_args()

    if args.mode == "2D":
        from display import AlgorithmTester, Dijkstra_wrapper, aStar_wrapper, GBFS_wrapper
        if args.level == 1 or args.level == 2: 
            if args.search == "dijkstra":
                algorithms = [Dijkstra_wrapper]
            elif args.search == "astar":
                algorithms = [aStar_wrapper]
            elif args.search == "gbfs":
                algorithms = [GBFS_wrapper]
            elif args.search == "dynamic":
                pass
            else:
                pass


            input_folder = f'Test_cases_level1&2'
            output_folder = f'Results_level1&2'

            tester = AlgorithmTester(algorithms, input_folder, output_folder)
            tester.run_tests()
            
        elif args.level == 3 and args.search == "astar":
            algorithms = [aStar_wrapper]
            input_folder = f'Test_cases_level3'
            output_folder = f'Results_level3'

            tester = AlgorithmTester(algorithms, input_folder, output_folder)
            tester.run_tests()
        else:
            pass

    elif args.mode == "3D":
        from display_3D import AlgorithmTester_3D,Dijkstra_wrapper, aStar_wrapper, GBFS_wrapper
        
        if args.search == "dijkstra":
                algorithms = [Dijkstra_wrapper]
        elif args.search == "astar":
            algorithms = [aStar_wrapper]
        elif args.search == "gbfs":
            algorithms = [GBFS_wrapper]

        input_folder = f'Test_cases_3D'
        output_folder = f'Results_3D'

        tester = AlgorithmTester_3D(algorithms, input_folder, output_folder)
        tester.run_tests()
        
    else:
        pass

if __name__ == "__main__":
    #python main.py -level 1 -mode 2D -search dijkstra
    main()
