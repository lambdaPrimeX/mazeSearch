class Node():
    def __init__(self,row,col):
        self.order = None
        self.type = None            # DE - Dead-End; TAR - Target; L/R/CO - Left/Right/Corner.
        self.position = (row,col)   # coordinates of node 
        self.edge = [ [None,None] ] # [ [ID,weight],[ID,weight] ]
        self.weight = None
        self.associate_qty = 0