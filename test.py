class Node:
    def __init__(self):
        self.nodes = []
    
    def addchildren(self):
        self.nodes.append(Node())
        self.nodes.append(Node())