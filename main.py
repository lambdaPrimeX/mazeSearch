from PIL import Image
import os
import sys
from classMaze import Maze

if os.path.exists(sys.argv[1]):
    path = os.path.basename(sys.argv[1])
    img = Image.open(path)
else:
    print("no image found.")
    exit()

maze = Maze(img)         # Construct maze
maze.prepare_image(img)  # MAKE img boolean, invert, delete edges
maze.find_vector_space() # Generates Tuple-Pair for range of coordinate space
maze.find_cor_enter_exit()
maze.set_nodes()
maze.print_nodes()