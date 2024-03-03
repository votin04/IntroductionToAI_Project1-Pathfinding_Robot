from queue import PriorityQueue
from map import *
import math
import heapq

# def h(cell1, cell2):
#     x1,y1 = cell1
#     x2,y2 = cell2
#     return abs(x1 - x2) + abs(y1 - y2)

# def aStar(m, start=None, end=None):
#     #list of coordinates of all cells in the grid
#     grid = m.grid()
#     directions=["L","R","U", "D", "UL", "UR", "DL", "DR"]

#     #declare first value for the g_score and f_score to calculate distance
#     g_score={cell:float('inf') for cell in grid}
#     g_score[start]= 0
#     f_score={cell:float('inf') for cell in grid}
#     f_score[start]=h(start, end)

#     #open the priority queue
#     open=PriorityQueue()
#     open.put((h(start, end), h(start, end), start))

#     #declare the dictionary to hold the path from start to goal, each node will store it's parent as the value and it will be the key 
#     aPath={}

#     while not open.empty():
#         #get the value of the calculating point
#         currCell=open.get()[2]
#         if currCell==(1,1):
#             break
#         for d in directions:
#             if d=="L":
#                 childCell=(currCell[0], currCell[1]-1)
#             if d=="R":
#                 childCell=(currCell[0], currCell[1]+1)
#             if d=="U":
#                 childCell=(currCell[0]-1, currCell[1])
#             if d=="D":
#                 childCell=(currCell[0]+1, currCell[1])
#             if d=="UL":
#                 childCell=(currCell[0]-1, currCell[1]-1)
#             if d=="UR":
#                 childCell=(currCell[0]-1, currCell[1]+1)
#             if d=="DL":
#                 childCell=(currCell[0]+1, currCell[1]-1)
#             if d=="DR":
#                 childCell=(currCell[0]+1, currCell[1]+1)
            
#             x,y=childCell

#             if m.matrix[x][y]==0:
            
#             # if m.maze_map[currCell][d]==True:
#             #     if d=='E':
#             #         childCell=(currCell[0], currCell[1]+1)
#             #     if d=='W':
#             #         childCell=(currCell[0], currCell[1]-1)
#             #     if d=='N':
#             #         childCell=(currCell[0]-1, currCell[1])
#             #     if d=='S':
#             #         childCell=(currCell[0]+1, currCell[1])

#                 temp_g_score=g_score[currCell]+1
#                 temp_f_score=temp_g_score + h(childCell, (1,1))

#                 if temp_f_score < f_score[childCell]:
#                     g_score[childCell] = temp_g_score
#                     f_score[childCell] = temp_f_score
#                     open.put((temp_f_score, h(childCell,(1,1)), childCell))
#                     aPath[childCell]=currCell

#     fwdPath={}
#     cell=(1,1)

#     #this while loop will execute on the path from the goal to the start point
#     while cell != start:
#         fwdPath[aPath[cell]]=cell
#         cell=aPath[cell]
#     return fwdPath

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.g = float('inf')
        self.h = 0

def is_valid(row, col, max_rows, max_cols):
    return (row >= 0) and (row < max_rows) and (col >= 0) and (col < max_cols)

def is_unblocked(grid, row, col):
    return grid[row][col] == 2 or grid[row][col] == 4 or grid[row][col] == 0

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5
 
def trace_path(cell_details, dest):
    print("The Path is ")
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
 
    # Print the path
    for i in path:
        print("->", i, end=" ")
    print()
    return path
 
def aStar(matrix, src, dest):
    max_rows, max_cols = matrix.shape
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1], max_rows, max_cols) or not is_valid(dest[0], dest[1], max_rows, max_cols):
        print("Source or destination is invalid")
        return
 
    # Check if the source and destination are unblocked
    if not is_unblocked(matrix, src[0], src[1]) or not is_unblocked(matrix, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return
 
    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
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
            if is_valid(new_i, new_j, max_rows, max_cols) and is_unblocked(matrix, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    found_dest = True 
                    return path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
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
 

'''TESTING SECTION'''                  
map = Map()
map.create('input.txt')

matrix = map.matrix

src = []
des = []

src.append(map.map_info.points['start'][1])
src.append(map.map_info.points['start'][0])

des.append(map.map_info.points['end'][1])
des.append(map.map_info.points['end'][0])

path = aStar(matrix, src, des)

# Display the matrix
matplotlib.use('Agg')
plt.imshow(map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

# Add colorbar for reference
plt.colorbar()
plt.title('Map Matrix')
plt.savefig("matplotlib.png")