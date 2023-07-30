import numpy as np
from classNode import Node
from classMarker import Marker

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
            cor = i
            if col_enter[i]:
                self.entrance   = (0,cor)
            if col_exit[i]:
                self.goal_state = (30,cor)

    def print_nodes(self):
        for i in range(0,len(self.nodes)):
            print("ID:", self.nodes[i].ID,"  \t(X,Y):",self.nodes[i].position,"  \tTYPE:",self.nodes[i].type)

    def direction(self,row,col):

        Lrow = row
        Lcol = col-1

        Rrow = row
        Rcol = col+1
        
        Urow = row-1
        Ucol = col
        
        Drow = row+1
        Dcol = col

        return (Lrow,Lcol),(Rrow,Rcol),(Urow,Ucol),(Drow,Dcol)

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

                # Lrow,Lcol,Rrow,Rcol,Urow,Ucol,Drow,Dcol = self.direction(row,col)
                # L,R,U,D = self.direction(row,col)

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

                # print("TEST: ", L)

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

    def create_edges(self):
        self.nodes[1].edge = [[1,2]]    #(u,v) (weight,connected vertex)
        # give each edge property [ [L,(u,v)] , [R,(u,v)], [U,(u,v)], [D,(u,v)] ]

# need to creat action, stepping left, right up or down. Think of way to organise and associate clear 

    # def move(self):
    #         # row = trav[i][0]    # (y-coordinate) | (y,x)
    #         # col = trav[i][1]    # (x-coordinate) | (y,x)

    #         row = self.location[0][0]
    #         col = self.location[1][0]

    #         Lrow,Lcol,Rrow,Rcol,Urow,Ucol,Drow,Dcol = self.direction(row,col)

    #         Dcol = col
    #         self.location = (Urow,Ucol)
    
    def initialise_path(self):
        self.marker = Marker()
        self.marker.current = self.entrance # [(row,col),[("L",False),("R",False)...]
        self.find_possible_moves()

    def find_possible_moves(self):
        # ROW = X[0], COL = X[1]
        # current = self.marker.current
        L,R,U,D = self.direction(self.marker.current[0],self.marker.current[1]) 
        # ,Lrow = L[1]s
        # Rrow,Rcol
        # Urow,Ucol
        # Drow,Dcol
        self.marker.L.cor = L
        self.marker.R.cor = R
        self.marker.U.cor = U
        self.marker.D.cor = D
        
        self.marker.L.truth = self.array[L]
        self.marker.R.truth = self.array[R]
        self.marker.U.truth = self.array[U]
        self.marker.D.truth = self.array[D]

        print("\nL:",self.marker.L.cor,self.marker.L.truth,"\tR:",self.marker.R.cor,self.marker.R.truth,"\tU:",self.marker.U.cor,self.marker.U.truth,"\tD:",self.marker.D.cor,self.marker.D.truth,"\n")
        # loc.append(direction)
        # print(loc)
        # # lo
        # return direction

    def order_nodes_by_proximity(self):
        # moves = self.find_possible_moves()
        # self.move(direction)
        # print("marker 2:",self.marker.L)
        print("----------")

    # Function to determine next move,
    # Evaluate all of the surrounding cells
        # if True, explore until node is discorvered

    # Function to search list nodes[i] if == then return as next in position

    def move_to_valid_cell(self):
        # print(self.marker.D.cor)
        validPath = []
        # check truth of each L,R,U,D, if true then 
        if(self.marker.L.truth == True):
            validPath.append(self.marker.L.cor)
        if(self.marker.R.truth == True):
            validPath.append(self.marker.R.cor)
        if(self.marker.U.truth == True):
            validPath.append(self.marker.U.cor)
        if(self.marker.D.truth == True):
            validPath.append(self.marker.D.cor)

        self.marker.validPath = validPath

    # def match_nodes_list(self,check):
    #     nodes = self.nodes
    #     for i in range(len(nodes)):
    #         if check == nodes[i].position:
    #             next.nodes[i]
    #     return next