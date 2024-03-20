# Instructions for Using the Program

This program is designed to process input files according to specified levels and search algorithms. Below are the instructions on how to use it effectively:

## Usage Syntax

The program should be run using the following syntax:

python main.py -filepath <file_path> -level <level_number> -search <search_algorithm>


Where:
- `-filepath` or `-f`: Specifies the input file path, which can be either a relative or absolute path.
- `-level` or `-l`: Specifies the level of the project requirements to run (1-5).
- `-search` or `-s`: Specifies the search algorithm to use. Available options are:
  - Dijkstra: "dijkstra"
  - A* search: "astar"
  - Greedy Best First Search: "gbfs"

## Notes

- By default, level 3 only supports the A* search algorithm.
- Parameters in the file must be compatible with the specified levels, such as having pickup points or not, 2D or 3D maps.

## Examples

### Example 1:

python main.py -f input.txt -l 3

- This command runs the program on the `input.txt` file.
- It uses the level 3 map.
- By default, it employs the A* search algorithm.

### Example 2:

python main.py -f input.txt -l 3 -s dijkstra

- This command runs the program on the `input.txt` file.
- It uses the level 3 map.
- Since the Dijkstra algorithm is specified, it will display an error message stating that level 3 only supports A* search.

### Example 3:

python main.py -filepath input.txt -level 5 -search gbfs

- This command runs the program on the `input.txt` file.
- It uses the level 5 map (3D).
- It utilizes the Greedy Best First Search algorithm.

