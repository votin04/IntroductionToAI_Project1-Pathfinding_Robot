
# Import the heapq module to implement the priority queue
import heapq

# Define the space limit, the start point, the end point and the polygons
space_limit = (22,18)
start, end = (2,2), (19,16)
polygons = [
    [(4,4), (5,9), (8,10), (9,5)],
    [(8,12), (8,17), (13,12)],
    [(11,1), (11,6), (14,6), (14,1)]
]

# Define a function to calculate the Euclidean distance between two points
def euclidean(p1, p2):
    # Unpack the coordinates of the points
    x1, y1 = p1
    x2, y2 = p2
    # Calculate the distance using the formula
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    # Return the distance
    return distance


# Define a function to check if a point is inside any polygon
def is_inside_polygon(point, polygons):
    x, y = point
    oddNodes = False
    # Loop through all the polygons
    for polygon in polygons:
        j = len(polygon) - 1
        # Loop through all the edges of the polygon
        for i in range(len(polygon)):
            xi, yi = polygon[i][:2]
            xj, yj = polygon[j][:2]
            # Check if the point is between the y-coordinates of the edge
            if (yi < y and yj >= y) or (yj < y and yi >= y):
                # Check if the point is to the left of the edge
                if xi + ((y - yi) / (yj - yi)) * (xj - xi) < x:
                    # Toggle the oddNodes flag
                    oddNodes = not oddNodes
            j = i
        # If the point is inside the polygon, return True
        if oddNodes:
            return True
    # If the point is not inside any polygon, return False
    return False


# Define a function to check if a line segment crosses any polygon
def is_crossing_polygon(p1, p2, polygons):
    # Loop through all the polygons
    for polygon in polygons:
        j = len(polygon) - 1
        # Loop through all the edges of the polygon
        for i in range(len(polygon)):
            # Get the coordinates of the edge
            x1, y1 = polygon[i][:2]
            x2, y2 = polygon[j][:2]
        
            s1_x = p2[0] - p1[0]
            s1_y = p2[1] - p1[1]
            s2_x = x2 - x1
            s2_y = y2 - y1
            # Calculate the denominator
            denom = (-s2_x * s1_y + s1_x * s2_y)
            # Check if the denominator is zero
            if denom == 0:
                # The line segments are parallel, return False
                return False
            # Otherwise, calculate the numerator and the fraction
            s = (-s1_y * (p1[0] - x1) + s1_x * (p1[1] - y1)) / denom
            t = ( s2_x * (p1[1] - y1) - s2_y * (p1[0] - x1)) / denom
            # Check if the fraction is between 0 and 1
            if 0 <= s <= 1 and 0 <= t <= 1:
                # The line segments intersect, return True
                return True
            j = i
    # If the line segment does not cross any polygon, return False
    return False



# Define a function to implement the greedy best first search algorithm
def greedy_best_first_search(start, end, map_obj):
    queue = [(euclidean(start, end), start)]
    visited = set()  # Initialize the set of visited points
    parent = {}  # Initialize the dictionary of parent points
    
    # Add the start point to visited set
    visited.add(start)
    
    while queue:
        cost, current = heapq.heappop(queue)
        if current == end:
            path = [end]
            while current in parent:
                current = parent[current]
                path.append(current)
            path.reverse()
            return path, cost
        # Add diagonal movements
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x = current[0] + dx
            y = current[1] + dy
            
            if 0 <= x < map_obj.map_info.map_limits['col_num'] and 0 <= y < map_obj.map_info.map_limits['row_num'] and map_obj.matrix[y][x] != 1 and (x, y) not in visited:
                h = euclidean((x, y), end)
                heapq.heappush(queue, (h, (x, y)))
                visited.add((x, y))  # Mark the current point as visited
                parent[(x, y)] = current
    return None



# # Call the function and print the result
# path, cost = greedy_best_first_search(start, end, polygons)
# print(path)

import matplotlib as plt
import matplotlib
from map import *

'''TESTING SECTION'''                  
map = Map()
map.create('./Test_cases/maximum_obstacles.txt')
# print(map.map_info.map_limits)
# print(map.map_info.points)
# print(map.map_info.obstacles)
path, cost = greedy_best_first_search(map.map_info.points['start'], map.map_info.points['end'], map)

# Display the matrix
matplotlib.use('Agg')
plt.imshow(map.matrix, cmap='viridis', interpolation='nearest', origin='lower')

shortest_path = np.array(path)
plt.plot(shortest_path[:, 1], shortest_path[:, 0], 'go', markersize=5, alpha=0.5)

# Add colorbar for reference
plt.colorbar()
plt.title('Map Matrix')
plt.savefig("GBFS.png")