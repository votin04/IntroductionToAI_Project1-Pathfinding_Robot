#Chạy code ở đây

'''ĐANG TEST NHÁP THỬ COI THUẬT TOÁN CHẠY ĐÚNG KO THÔI'''
from map import *
from GBFS import *

'''TESTING SECTION'''                  
map = Map()
map.create('input.txt')
# print(map.map_info.map_limits)
# print(map.map_info.points)
# print(map.map_info.obstacles)
path, cost = greedy_best_first_search(map.map_info.points['start'], map.map_info.points['end'], map)

for point in path:
    print(f"[{point[1]},{point[0]}]")
    map.matrix[point[1]][point[0]] = 3

# Display the matrix
matplotlib.use('Agg')
plt.imshow(map.matrix, cmap='viridis', interpolation='nearest', origin='lower')
# Add colorbar for reference
plt.colorbar()
plt.title('Map Matrix')
plt.savefig("matplotlib.png")