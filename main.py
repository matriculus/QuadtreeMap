# import libraries
from matplotlib import pyplot as plt

k = 4
WIDTH = 640
HEIGHT = WIDTH

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.w = self.p2[0] - self.p1[0]
        self.h = self.p2[1] - self.p1[1]
        self.x = [self.p1[0], self.p2[0]]
        self.y = [self.p1[1], self.p2[1]]
    
    def __str__(self):
        # self.plot()
        return f"P1: {self.p1}\tP2: {self.p2}"
    
    def plot(self):
        plt.plot(self.x, self.y)

class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary = boundary
        self.children = []
        self.parent = None
    
    def addChild(self, child):
        if len(self.children) < k:
            child.parent = self
            self.children.append(child)
        else:
            print(f"No. of children exceeding {k}!")
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def print_tree(self):
        prefix = f"{self.get_level()} "
        spacer = ' ' * self.get_level()*3 + "|__" if self.parent else ""
        statement = prefix + spacer + f"{self.boundary}"
        print(statement)
        if self.children:
            for child in self.children:
                child.print_tree()
        plt.show()
    
    def add_level(self):
        P1 = self.boundary.p1
        P2 = self.boundary.p2
        width = self.boundary.w
        height = self.boundary.h
        # nw point
        p1 = P1
        p2 = P1[0] + width/2, P1[1] + height/2
        self.addChild(QuadTreeNode(Rectangle(p1, p2)))
        # sw point
        p1 = P1[0], P1[1] + height/2
        p2 = P1[0] + width/2, P1[1] + height
        self.addChild(QuadTreeNode(Rectangle(p1, p2)))
        # se point
        p1 = P1[0] + width/2, P1[1] + height/2
        p2 = P2
        self.addChild(QuadTreeNode(Rectangle(p1, p2)))
        # ne point
        p1 = P1[0] + width/2, P1[1]
        p2 = P2[0], P1[1] + height/2
        self.addChild(QuadTreeNode(Rectangle(p1, p2)))

boundbox = Rectangle((0,0), (WIDTH, HEIGHT))
levels = 4
root = QuadTreeNode(boundbox)
root.add_level()
for child1 in root.children:
    child1.add_level()
    for child2 in child1.children:
        child2.add_level()
        for child3 in child2.children:
            child3.add_level()
            for child4 in child3.children:
                child4.add_level()


root.print_tree()