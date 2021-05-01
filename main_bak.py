# import libraries

k = 4
WIDTH = 640
HEIGHT = WIDTH
maxLevel = 4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def __str__(self):
        p1 = (self.x, self.y)
        p2 = (self.x + self.w, self.y + self.h)
        return f"|P1: {p1}|\t|P2: {p2}|"
    
    def contains(self, point):
        if point.x > self.x and point.y > self.y:
            if point.x < self.x + self.w and point.y < self.y + self.h:
                return True
        return False

class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary = boundary
        self.children = []
        self.parent = None
        self.occupancy = False
    
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
        spacer = ' ' * self.get_level()*3 + "|____" if self.parent else ""
        statement = prefix + spacer + f"{self.boundary}" + f"\tOccupied: {self.occupancy}" + f"\t# children: {len(self.children)}"
        print(statement)
        if self.children:
            for child in self.children:
                child.print_tree()
    
    def add_level(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        # nw point
        self.addChild(QuadTreeNode(Rectangle(x, y, w/2, h/2)))
        # sw point
        self.addChild(QuadTreeNode(Rectangle(x, y + h/2, w/2, h/2)))
        # se point
        self.addChild(QuadTreeNode(Rectangle(x + w/2, y + h/2, w/2, h/2)))
        # ne point
        self.addChild(QuadTreeNode(Rectangle(x + w/2, y, w/2, h/2)))
    
    def add_until_level(self, maxlevel):
        if maxlevel <= self.get_level() : return
        self.add_level()
        for child in self.children: child.add_until_level(maxlevel)
    
    def insert(self, point):
        if maxLevel <= self.get_level():
            if self.boundary.contains(point):
                self.occupancy = True
            return
        
        if self.boundary.contains(point):
            # self.occupancy = True
            if len(self.children) > 0:
                print("has children")
                for child in self.children:
                    child.insert(point)
            print("do not have children")
            self.add_level()
            for child in self.children:
                child.insert(point)
            # self.children = [child for child in self.children if child.occupancy]  
            # print(self.isOccupied())
        return
    
    def isOccupied(self):
        if len(self.children) == 0:
            return self.occupancy
        
        for child in self.children:
            child.isOccupied()
        



boundbox = Rectangle(0, 0, WIDTH, HEIGHT)
root = QuadTreeNode(boundbox)
root.insert(Point(0.125, 0.156))
print("=================")
root.insert(Point(1,1))
root.print_tree()