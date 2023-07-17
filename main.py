from PIL import Image
import os
import sys
import numpy as np
from classConstructor import *

class Node():
    def __init__(self,row,col):
        self.order = None
        self.type = None # DE - Dead-End; TAR - Target; L/R/CO - Left/Right/Corner.
        self.position = (row,col) # coordinates of node 
        self.edge = [ [None,None] ] # [ [ID,weight],[ID,weight] ]
        self.associate_qty = 0

class Maze():
    def __init__(self,img):
        self.image  = img
        self.width  = img.width -1
        self.height = img.height -1
        self.dim    = self.height * self.width

    def prepare_image(self,img):

        # Make image array      (1)
        # Invert boolean values (2)
        # Delete bottom row     (3)
        # Delete end column     (4)
# IMPROVE   - make additional strip on all four edges of all false, so when [-1] doesnt fail in the event the start and target are on the sale row*col or col*row
        img_arr = np.array(img)         # (1)
        img_inv = np.invert(img_arr)    # (2)
        img = np.delete(img_inv,-1,0)   # (3)
        img = np.delete(img,-1,-1)      # (4)

        self.array = img

    def find_vector_space(self):
        self.span = (len(self.array[:,0]),len(self.array[0,:]))

    def find_cor_enter_exit(self):
        col_enter = self.array[0]
        col_exit  = self.array[-1]

        for i in range(0,len(col_enter)):
            cor = i         # +1 convert to coordinate
            if col_enter[i]:
                self.entrance = (0,cor)
            if col_exit[i]:
                self.exit     = (30,cor)

    def set_nodes(self):
        def traversable():
            set = []            # <- (None,None)
            vis = (None,None)   # <- (None,None)

            for x in range(self.width):
                for y in range(self.height):
                    vis = (x,y)
                    if self.array[vis]:
                        set.append(vis)
            return set
        
        def inspect_cor(trav):

            def cardinality(set):
                set_size = 0
                for i in range(len(set)):
                    if(not set[i]):
                        set_size += 1
                return set_size

            nodes = []

            # Identify nodes of interest, to prevent searching every pixel
            for i in range(len(trav)-1):

                # print(trav)
                # print(trav[38])
                row = trav[i][0]    # (x-coordinate)
                col = trav[i][1]    # (y-coordinate)
                # row = 9
                # col = 15
                # print(row,col)
    # print(maze.array[row,col])

                # inspect UP
                # if(maze.array[row-1,col]):
                #     print("out of bounds")

                Lrow = row
                Lcol = col-1
                
                Rrow = row
                Rcol = col+1
                
                Urow = row-1
                Ucol = col

                Drow = row+1
                Dcol = col

                L = maze.array[Lrow,Lcol]
                R = maze.array[Rrow,Rcol]
                U = maze.array[Urow,Ucol]
                D = maze.array[Drow,Dcol]

                neighbours = []
                neighbours.append(L)
                neighbours.append(R)
                neighbours.append(U)
                neighbours.append(D)

                set_size = cardinality(neighbours)
                # print(set_size)

                # i = 1

                if(set_size < 3):
                    # AGGREGATE into one conditional wich labels TYPE as COR
                    # identify a corner
                    if((maze.array[row,col]) and (not maze.array[Lrow,Lcol]) and (not maze.array[Urow,Ucol])):
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                        # print("Left-Down Corner: ",node.position)
                    if((maze.array[row,col]) and (not maze.array[Rrow,Rcol]) and (not maze.array[Urow,Ucol])):
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                        # print("Right-Down Corner: ",node.position)
                    if((maze.array[row,col]) and (not maze.array[Lrow,Lcol]) and (not maze.array[Drow,Dcol])):
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                        # print("Left-Up Corner: ",node.position)
                    if((maze.array[row,col]) and (not maze.array[Rrow,Rcol]) and (not maze.array[Drow,Dcol])):
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                        # print("Right-Up Corner: ",node.position)
                    
                    # node.ID = i
                    # nodes.append(node)

                if(set_size == 3):
                    # identify a Dead-End
                    if((maze.array[row,col]) and (not maze.array[row,col-1]) and (not maze.array[row,col+1]) and (not maze.array[row-1,col])):
                        node = Node(row,col)
                        node.type = "DE"
                        # print("Dead-End Up: ",node.position)                    
                        node.ID = i
                        nodes.append(node)


                # CREATE conditional for T junction
            
            # print(nodes[i].position)
            return nodes

        # cycle through each pixel in each row, identify points of interest, put them in que from order 
        trav = traversable()
        nodes=[]
        nodes = inspect_cor(trav)

        for i in range(0,len(nodes)):
            print("ID:", nodes[i].ID,"  \t(X,Y):",nodes[i].position,"  \tTYPE:",nodes[i].type)
        
        # print(trav)
        # for i in range(0,5):
        #     inspect_cor(cue[i])
        # for i in range(len(cue)):
        
        #     # if coordinate of interest
        #     if(inspect_cor(cue[i])):
        #         print(cue[i])
                # make into a node and store
                # node = Node(cue[i])
                # node.edge
                # cue.append(Node(cue[i]))
            
                    
                    # "ID $'f" = Node()
                    # print(vis)      # IMPORTANT - all of these are traversable coordinates
                        # Visit each coordinate in sequence
                            # For each cor that has a TYPE make it a node
                                # Place into a preliminary cue awaiting ordering

                    # NEXT -> need to visit each coordinate and give state/type

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
# print(maze.exit)
# print(maze.span[0])
# print(maze.array[-1])
# print(maze.dim)