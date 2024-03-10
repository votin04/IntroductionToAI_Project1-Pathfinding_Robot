from queue import PriorityQueue
from map import *
import math
import heapq
import itertools
class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.g = float('inf')
        self.h = 0
class AStar:
    def __init__(self, matrix, points):
        self.matrix = matrix
        self.points = points

        for i in range(len(points)):
            self.points[i] = self.reverse_tuple(self.points[i])
        

    def is_valid(self, row, col, max_rows, max_cols):
        return (row >= 0) and (row < max_rows) and (col >= 0) and (col < max_cols)

    def is_unblocked(self, grid, row, col):
        return grid[row][col] == 2 or grid[row][col] == 4 or grid[row][col] == 3 or grid[row][col] == 0

    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    def calculate_h_value(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5
    
    def trace_path(self, cell_details, dest):
        path = []
        row = dest[0]
        col = dest[1]
    
        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col
    
        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()
    
        return path
    
    def aStar(self, src, des):
        max_rows, max_cols = self.matrix.shape
        # Check if the source and destination are valid
        if not self.is_valid(src[0], src[1], max_rows, max_cols) or not self.is_valid(des[0], des[1], max_rows, max_cols):
            print("Source or destination is invalid")
            return
    
        # Check if the source and destination are unblocked
        if not self.is_unblocked(self.matrix, src[0], src[1]) or not self.is_unblocked(self.matrix, des[0], des[1]):
            # print("Source or the destination is blocked")
            return
    
        # Check if we are already at the destination
        if self.is_destination(src[0], src[1], des):
            # print("We are already at the destination")
            return
    
        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(max_cols)] for _ in range(max_rows)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(max_cols)] for _ in range(max_rows)]
    
        # Initialize the start cell details
        i = src[0]
        j = src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j
    
        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False
    
        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)
    
            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True
    
            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]
    
                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j, max_rows, max_cols) and self.is_unblocked(self.matrix, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j, des):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        # print("The destination cell is found")
                        # Trace and print the path from source to destination
                        path = self.trace_path(cell_details, des)
                        found_dest = True 
                        return path
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j, des)
                        f_new = g_new + h_new
    
                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j
    
        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")

    def reverse_tuple(self, t):
        new_tuple = ()
        for i in range(len(t)-1, -1, -1):
            new_tuple += (t[i],)
        return new_tuple

    def findPickUp(self):
        size = len(self.points) + 2

        # Initialize distance matrix with zeros
        result = [[0] * size for _ in range(size)]

        # Create a list containing start, end, and all points
        startPoint = self.src
        endPoint = self.des

        point_list = [startPoint] + self.points + [endPoint]

        # Calculate distances and populate the matrix
        for i, (x1, y1) in enumerate(point_list):
            for j, (x2, y2) in enumerate(point_list):
                # Calculate Euclidean distance between points
                startList = []
                endList = []

                startList.append(y1)
                startList.append(x1)

                endList.append(y2)
                endList.append(x2)

                path = self.aStar(startList, endList)
                if path != None:
                    result[i][j] = len(path)
        
        # Add index for the maze point 
        startPoint += (0,)
        endPoint   += (size - 1,)
        index = 1

        for i in range(len(self.points)):
            self.points[i] += (index,)
            index += 1
        
        # Using Permutation To Check Traverse Random PickUp Points
        permutatePath =  list(itertools.permutations(self.points))

        paths = []
        # Concatenate start and end points to each permutation
        for perm in permutatePath:
        # Concatenate start and end points to each permutation
            path = [startPoint] + list(perm) + [endPoint]
            paths.append(path)

        # Calculate the total cost from path
        max = 1000000
        total = 0
        for path in paths:
            for i in range(len(path)-1):
                # Sum the path from one node to another node
                total += result[path[i][2]][path[i+1][2]]
            if max > total:
                max = total
                shortestPath = path
        
        res = []
        for i in shortestPath:
            i = list(i)
            i.pop(2)
            res.append(tuple(i))

        finalPath = []

        for i in range(len(res) - 1):
            path = self.aStar(res[i], res[i+1])
            finalPath = finalPath + path[1:]

        return finalPath

    
# '''TESTING SECTION'''  

# ''''
#     To use the AStar Function please use the reverse_tuple from AStar class in order to use the aStar function
# '''
# # Create a map             
# map = Map()
# map.create('./Test_cases/test1.txt')
# matrix = map.matrix
# points = map.map_info.points['passing_points']
# src = map.map_info.points['start']
# des = map.map_info.points['end']

# searchPath = AStar(matrix, src, des, points)

# src = searchPath.reverse_tuple(src)
# des = searchPath.reverse_tuple(des)

# #path = searchPath.findPickUp()
# path = searchPath.aStar(src, des)

# # Display
# matplotlib.use('Agg')
# plt.imshow(map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

# shortest_path = np.array(path)
# plt.plot(shortest_path[:, 1], shortest_path[:, 0], 'go', markersize=5, alpha=0.5)

# plt.colorbar()
# plt.title('Map Matrix')
# plt.savefig("aStar.png")