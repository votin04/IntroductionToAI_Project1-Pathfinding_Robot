import argparse
from map import *
from map_3D import *
from aStar import *
from GBFS import *
from Dijkstra import *
from display import *
from display_3D import *
from display_dynamic import *
from algorithm_runner import *

def main():
    parser = argparse.ArgumentParser(description="Pathfinding Robot")

    parser.add_argument("-filepath", "-f" , type=str, required=True)
    parser.add_argument("-level","-l", type=int, required=True)
    parser.add_argument("-search", "-s",choices=["dijkstra", "astar", "gbfs"], required=False)

    args = parser.parse_args()

    
    if args.level == 3 and not args.search:
        args.search = "astar"
        
    if not args.filepath:
        raise Exception("Error: Please provide the -filepath option!!!")
        
    if not args.level:
        raise Exception("Error: Please provide the -level option!!!")
        
    if not args.search:
        raise Exception("Error: Please provide the -search option!!!")
        
    if args.level < 1 or args.level > 5:
        raise Exception("Error: Invalid level. Please provide a level between 1 and 5!!!")
        
    if args.level == 3 and args.search != "astar":
        raise Exception("Error: The program runs only A* algorithm for level 3!!!")
    
    map_class = {
        1: Map,
        2: Map,
        3: Map,
        4: Map,
        5: Map_3D,
    }

    displayer_class = {
        1: Displayer,
        2: Displayer,
        3: Displayer,
        4: Displayer_dynamic,
        5: Displayer_3D
    }

    algorithm_class = {
        "dijkstra" : Dijkstra_wrapper,
        "astar" : aStar_wrapper,
        "gbfs" : GBFS_wrapper
    }

    output_folder = {
        1: "Results_level1",
        2: "Results_level2",
        3: "Results_level3",
        4: "Results_level4",
        5: "Results_level5"
    }

    runner = AlgorithmRunner(map_class[args.level], algorithm_class[args.search], displayer_class[args.level], args.filepath, output_folder[args.level])
    runner.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)