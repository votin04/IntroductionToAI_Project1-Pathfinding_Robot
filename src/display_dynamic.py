import os
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

        self.map.generator = map.generator

    def draw(self, path, cost, name, output_folder):
        if len(path) > 1:
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
                    image = displayer.draw(renderPath, cnt, " ", "Results_level4")

                    images.append(imageio.v2.imread(image))    

            if os.path.exists(f"{output_folder}/") == False:
                os.makedirs(f"{output_folder}/")

            video_name = f"{output_folder}/{name}_dynamic.gif"

            imageio.v2.mimsave(video_name, images, duration=500)
            
            os.remove(image)

        else:
            print("No path found. Cannot create a gif.")