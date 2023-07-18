import numpy as np
from classNode import Node

class Maze():
    def __init__(self,img):
        self.image  = img
        self.width  = img.width -1
        self.height = img.height -1
        self.dim    = self.height * self.width

    def prepare_image(self,img):

        #--------------------------
        # Make image array      (1)
        # Invert boolean values (2)
        # Delete bottom row     (3)
        # Delete end column     (4)
        #--------------------------

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

    def print_nodes(self):
        for i in range(0,len(self.nodes)):
            print("ID:", self.nodes[i].ID,"  \t(X,Y):",self.nodes[i].position,"  \tTYPE:",self.nodes[i].type)

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

                row = trav[i][0]    # (x-coordinate)
                col = trav[i][1]    # (y-coordinate)

                Lrow = row
                Lcol = col-1
                
                Rrow = row
                Rcol = col+1
                
                Urow = row-1
                Ucol = col

                Drow = row+1
                Dcol = col

                L = self.array[Lrow,Lcol]
                R = self.array[Rrow,Rcol]
                U = self.array[Urow,Ucol]
                D = self.array[Drow,Dcol]

                neighbours = []
                neighbours.append(L)
                neighbours.append(R)
                neighbours.append(U)
                neighbours.append(D)

                set_size = cardinality(neighbours)

                if(set_size < 3):
#CORNERS
                    if((self.array[row,col]) and (not self.array[Lrow,Lcol]) and (not self.array[Urow,Ucol])):
                    # LD-CORNER
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                    if((self.array[row,col]) and (not self.array[Rrow,Rcol]) and (not self.array[Urow,Ucol])):
                    # RD-CORNER
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                    if((self.array[row,col]) and (not self.array[Lrow,Lcol]) and (not self.array[Drow,Dcol])): 
                    # LU-CORNER
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
                    if((self.array[row,col]) and (not self.array[Rrow,Rcol]) and (not self.array[Drow,Dcol])):
                    # RD-CORNER
                        node = Node(row,col)
                        node.type = "COR"
                        node.ID = i
                        nodes.append(node)
#DEAD-END
                if(set_size == 3):
                    if((self.array[row,col]) and (not self.array[row,col-1]) and (not self.array[row,col+1]) and (not self.array[row-1,col])):
                        node = Node(row,col)
                        node.type = "DE"
                        node.ID = i
                        nodes.append(node)
                if(set_size == 1):
#JUNCTIONS
                    if( (not self.array[Urow,Ucol]) and (self.array[Lrow,Lcol]) and (self.array[Rrow,Rcol]) and (self.array[Drow,Dcol]) ):
                        node = Node(row,col)
                        node.type = "JUNC" # T-Junction
                        node.ID = i
                        nodes.append(node)
                    
                    if( (not self.array[Drow,Dcol]) and (self.array[Lrow,Lcol]) and (self.array[Rrow,Rcol]) and (self.array[Urow,Ucol]) ):
                        node = Node(row,col)
                        node.type = "JUNC" # 180DEG-T-Junction
                        node.ID = i
                        nodes.append(node)

                    if( (not self.array[Rrow,Rcol]) and (self.array[Lrow,Lcol]) and (self.array[Urow,Ucol]) and (self.array[Drow,Dcol]) ):
                        node = Node(row,col)
                        node.type = "JUNC" # 90DEG-T-Junction
                        node.ID = i
                        nodes.append(node)
                    
                    if( (not self.array[Lrow,Lcol]) and (self.array[Rrow,Rcol]) and (self.array[Urow,Ucol]) and (self.array[Drow,Dcol]) ):
                        node = Node(row,col)
                        node.type = "JUNC" # -90DEG-T-Junction
                        node.ID = i
                        nodes.append(node)
            return nodes

        # cycle through each pixel in each row, identify points of interest, put them in que from order 
        trav = traversable()
        nodes=[]
        nodes = inspect_cor(trav)

        self.nodes = nodes