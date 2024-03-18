from map import *

'''
Similar to Map class but added some information about third-dimension measurements
'''
class Map_3D(Map):
    def __init__(self) -> None:
        self.matrix = None
        self.map_info = MapInfo_3D()

    def create(self, file_name):
        generator = MapGenerator_3D()
        self.map_info = generator.import_file(file_name)
        self.matrix = generator.create_map()

'''
MapInfo_3D inherits from MapInfo:
- Still use matrix as a 2D matrix
- Store third_dimension mearsurements to display later: add height and add a list of 3D obstacles(same with 2D obstacles but have z-axis value)
'''
class MapInfo_3D(MapInfo):
    def __init__(self) -> None:
        super().__init__()
        self.map_limits['height'] = 0
        self.obstacles_3D = []

    def set_map_limits(self, col_num, row_num, height):
        super().set_map_limits(col_num, row_num)
        self.map_limits['height'] = height

    def add_obstacle_3D(self, obstacle):
        self.obstacles_3D.append(obstacle)

    def convert_obstacles_2D_to_3D(self):
        for obstacle in self.obstacles_3D:
            points = []
            for point in obstacle:
                points.append((point[0], point[1]))
            self.add_obstacle(points)


'''
MapGenerator_3D inherits from MapGenerator:
- Use MapInfo_3D class for map_info
- While reading data from file, it will parse data of 3D obstacles and convert them to 2D obstacles
'''
class MapGenerator_3D(MapGenerator):
    def __init__(self) -> None:
        self.map_info = MapInfo_3D()

    def import_file(self, file_name) -> MapInfo:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Read map limits
        map_limits = lines[0].strip().split(',')
        self.map_info.set_map_limits(int(map_limits[0]), int(map_limits[1]), int(map_limits[2]))

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
            shape = [(int(coordinates[i]), int(coordinates[i + 1]), int(coordinates[i + 2])) for i in range(0, len(coordinates), 3)]
            self.map_info.add_obstacle_3D(shape)
            current_line += 1
        self.map_info.convert_obstacles_2D_to_3D()

        return self.map_info
