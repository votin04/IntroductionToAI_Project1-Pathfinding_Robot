import numpy as np
import matplotlib
import matplotlib.pyplot as plt


'''Map class
Map is computationally interpreted as a matrix:
    empty cell: marked as 0.
    obstacle cell: marked as 1.
    start point: marked as 2.
    passing points: marked as 3.
    end point: marked as 4.
Map_info stores all necessary information of this map. To look for more detailed information, see MapInfo class implementation.
'''
class Map:
    def __init__(self) -> None:
        self.matrix = None
        self.map_info = MapInfo()
        self.generator = MapGenerator()

    def create(self, file_name):
        self.map_info = self.generator.import_file(file_name)
        self.matrix = self.generator.create_map()
    
    def createWithNewObstacles(self, obstacles):
        self.map_info.obstacles = obstacles
        self.matrix = self.generator.create_map()


'''Class used to store all necessary information about a map read from a text file'''
class MapInfo:
    def __init__(self) -> None:
        self.map_limits = {'col_num': 0, 'row_num': 0} # dictionary of numbers of column units and row units
        self.points = {'start': (0, 0), 
                       'end': (0, 0), 
                       'passing_points': []} # dictionary of points
        self.obstacles = [] # list of shapes where each shape is a list of point tuple
    
    def update_obstacles(self, dx, dy):
        for shape in self.obstacles:
            for i, (x, y) in enumerate(shape):
                # Update the coordinates in the list directly
                self.obstacles[self.obstacles.index(shape)][i] = (x + dx, y + dy)
        return self.obstacles


    def set_map_limits(self, col_num, row_num):
        self.map_limits['col_num'] = col_num
        self.map_limits['row_num'] = row_num

    def set_start_point(self, start_point):
        self.points['start'] = start_point

    def set_end_point(self, end_point):
        self.points['end'] = end_point

    def add_passing_point(self, passing_point):
        self.points['passing_points'].append(passing_point)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

'''Class used to generate a map given an input text file'''
class MapGenerator:
    def __init__(self) -> None:
        self.map_info = MapInfo()

    def import_file(self, file_name) -> MapInfo:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Read map limits
        map_limits = lines[0].strip().split(',')
        self.map_info.set_map_limits(int(map_limits[0]), int(map_limits[1]))

        # Read start points, end points
        point_coordinates = lines[1].strip().split(',')

        self.map_info.set_start_point((int(point_coordinates[0]), int(point_coordinates[1])))
        self.map_info.set_end_point((int(point_coordinates[2]), int(point_coordinates[3])))

        # Read passing points
        if len(point_coordinates) > 4:
            for i in range(4, len(point_coordinates), 2):
                self.map_info.add_passing_point((int(point_coordinates[i]), int(point_coordinates[i + 1])))

        # Read the number of obstacles
        num_obstacles = int(lines[2].strip())

        # Read obstacles
        current_line = 3
        for _ in range(num_obstacles):
            coordinates = lines[current_line].strip().split(',')
            shape = [(int(coordinates[i]), int(coordinates[i + 1])) for i in range(0, len(coordinates), 2)]
            self.map_info.add_obstacle(shape)
            current_line += 1

        return self.map_info

    def draw_line(self, x0, y0, x1, y1, matrix):
        # Bresenham's Line Algorithm
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while x0 != x1 or y0 != y1:
            matrix[y0, x0] = 1  # Mark obstacle cells as 1
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_shape(self, vertices, matrix):
        # Draw edges of the shape
        for i in range(len(vertices)):
            self.draw_line(vertices[i][0], vertices[i][1], vertices[(i + 1) % len(vertices)][0], vertices[(i + 1) % len(vertices)][1], matrix)

        # Scanline fill algorithm
        min_y = min(vertices, key=lambda p: p[1])[1]
        max_y = max(vertices, key=lambda p: p[1])[1]

        for y in range(min_y, max_y + 1):
            intersections = []

            for i in range(len(vertices)):
                x0, y0 = vertices[i]
                x1, y1 = vertices[(i + 1) % len(vertices)]

                if y0 <= y < y1 or y1 <= y < y0:
                    x_intersect = int((y - y0) / (y1 - y0) * (x1 - x0) + x0)
                    intersections.append(x_intersect)

            intersections.sort()

            for i in range(0, len(intersections), 2):
                for x in range(intersections[i], intersections[i + 1] + 1):
                    matrix[y, x] = 1  # Mark obstacle cells as 1

    def create_map(self):
        # Initialize a matrix with zeros
        map_matrix = np.zeros((self.map_info.map_limits['row_num'], self.map_info.map_limits['col_num']), dtype=int)
        # Mark start point
        start_point = self.map_info.points['start']
        map_matrix[start_point[1], start_point[0]] = 2

        # Mark end point
        end_point = self.map_info.points['end']
        map_matrix[end_point[1], end_point[0]] = 4

        # Mark passing points
        for passing_point in self.map_info.points['passing_points']:
            map_matrix[passing_point[1], passing_point[0]] = 3

        # Draw obstacles
        for obstacle in self.map_info.obstacles:
            self.draw_shape(obstacle, map_matrix)

        return map_matrix

    def extendObstacleBounds(self, map : Map):
        directions = [(1,0), (0,-1), (-1,0), (0,1) ]
        temp_map_info = MapInfo() # A temporary class to store adjusted obstacles's information
        temp_map_info.obstacles = map.map_info.obstacles

        # Iterate through all directions
        for dx, dy in directions:
            obstacles = temp_map_info.update_obstacles(dx, dy)
            for obstacle in obstacles:
                self.draw_shape(obstacle, map.matrix)

        return map