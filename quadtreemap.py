import tkinter as tk

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
        if len(self.children) < 4:
            child.parent = self
            self.children.append(child)
        else:
            print(f"No. of children exceeding 4!")
    
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
    
    def add_until_level(self, maxLevel):
        if maxLevel <= self.get_level() : return
        self.add_level()
        for child in self.children: child.add_until_level(maxLevel)
    
    def insert(self, point, maxLevel):
        if not self.boundary.contains(point):
            return
        
        if maxLevel <= self.get_level():
            if self.boundary.contains(point):
                self.occupancy = True
            return
        
        if len(self.children) > 0:
            for child in self.children:
                child.insert(point, maxLevel)
        else:
            self.add_level()
            for child in self.children:
                child.insert(point, maxLevel)
            # self.children = [child for child in self.children if child.isOccupied()]            
        
class QuadTree:
    def __init__(self, boundary, maxlevel):
        self.root = QuadTreeNode(boundary)
        self.maxLevel = maxlevel
    
    def insert(self, point):
        self.root.insert(point, self.maxLevel)
    
    def print_tree(self):
        self.root.print_tree()

class Tree(tk.Tk):
    pad = (100, 100)
    center = pad[0]/2, pad[1]/2
    r = 2
    def __init__(self, quadtree, width, height):
        tk.Tk.__init__(self)
        self.quadtree = quadtree
        self.cw, self.ch = width + self.pad[0], height + self.pad[1]
        self.createWindow()
    
    def createWindow(self):
        self.title("QuadTree Map")
        geo = f"{self.cw}x{self.ch}"
        self.geometry(geo)
        self.canvas = tk.Canvas(self, width = self.cw, height = self.ch, bg='#ffffff')
        self.canvas.pack()
        self.draw(self.quadtree)
    
    def loop(self):
        self.mainloop()

    def draw(self, quadtree):
        w = quadtree.boundary.w
        h = quadtree.boundary.h
        x1 = quadtree.boundary.x + self.center[0]
        y1 = quadtree.boundary.y + self.center[1]
        x2 = x1 + w
        y2 = y1 + h
        self.canvas.create_rectangle(x1, y1, x2, y2)
        if quadtree.children:
            for child in quadtree.children:
                self.draw(child)
        
    def draw_point(self, point):
        x = self.center[0] + point.x
        y = self.center[1] + point.y
        self.canvas.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill="black")