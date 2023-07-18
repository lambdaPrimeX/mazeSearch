from PIL import Image
import os
import sys
from classMaze import Maze

if (len(sys.argv) == 2):
    if os.path.exists(sys.argv[1]):
        path = os.path.basename(sys.argv[1])
        img = Image.open(path)
    else:
        print("WARNING: '",sys.argv[1],"' does not exist.")
        exit()
else:
    print("WARNING: no image given. Please specify 'main.py [image-source]'")
    exit()
if (len(sys.argv) > 2):
    print("WARNING: too many arguments given. Please specify 'main.py [image-source]'")
    exit()

maze = Maze(img)                # Construct maze
maze.prepare_image(img)         # MAKE img boolean, invert, delete edges
maze.find_vector_space()        # Generates Tuple-Pair for range of coordinate space
maze.find_cor_enter_exit()      # Finds start and target coordinates
maze.set_nodes()                # Finds all nodes of interest under maze.nodes unordered
maze.print_nodes()              # Testing print function for all nodes of interest
maze.create_edges()               # Gives edges and weight from start/entrance
maze.order_nodes_by_proximity() # Orders nodes by proximity to start
