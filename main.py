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

def match_nodes_list(self,check):
    nodes = self.nodes
    print("From F",check)
    for i in range(len(nodes)):
        if check == nodes[i].position:
            return True
        else:
            return False
        
self = Maze(img)
# self.nodes[0] = (1,1)
check = (1,1)

# self = Maze(img)                # Construct maze
# self.prepare_image(img)         # MAKE img boolean, invert, delete edges
# self.find_vector_space()        # Generates Tuple-Pair for range of coordinate space
# self.find_cor_enter_exit()      # Finds start and target coordinates
# self.set_nodes()                # Finds all nodes of interest under maze.nodes unordered
# print(match_nodes_list(self,check))
# print(self.nodes[1].position)



maze = Maze(img)                # Construct maze
maze.prepare_image(img)         # MAKE img boolean, invert, delete edges
maze.find_vector_space()        # Generates Tuple-Pair for range of coordinate space
maze.find_cor_enter_exit()      # Finds start and target coordinates
maze.set_nodes()                # Finds all nodes of interest under maze.nodes unordered
maze.create_edges()             # Gives edges and weight from start/entrance
maze.initialise_path()
maze.order_nodes_by_proximity() # Orders nodes by proximity to start
maze.print_nodes()              # Testing print function for all nodes of interest
# maze.create_valid_path_to_node()
