import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return self.print()
    
    def print(self):
        return f"X: {self.x}\tY: {self.y}"

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
    def __init__(self, boundary=None):
        self.boundary = boundary
        self.children = []
        self.parent = None
        self.occupancy = False
    
    def addChild(self, child):
        assert len(self.children) < 4
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
    
    def insertPoint(self, point, maxLevel):
        if not self.boundary.contains(point):
            return
        
        if maxLevel <= self.get_level():
            if self.boundary.contains(point):
                self.occupancy = True
            return
        
        if len(self.children) > 0:
            for child in self.children:
                child.insertPoint(point, maxLevel)
        else:
            if not self.occupancy:
                self.add_level()
                for child in self.children:
                    child.insertPoint(point, maxLevel)
        self.mergeOccupiedNodes()
    
    def insertPCData(self, pcData, maxLevel):
        if pcData:
            for point in pcData.getPoints():
                self.insertPoint(point, maxLevel)
            self.mergeOccupiedNodes()
    
    def insert(self, data, maxLevel):
        if isinstance(data, Point):
            self.insertPoint(data, maxLevel)
        elif isinstance(data, PointCloud):
            self.insertPCData(data, maxLevel)

    
    def mergeOccupiedNodes(self):
        occupancy = []
        if len(self.children) == 0:
            return
        for child in self.children:
            child.mergeOccupiedNodes()
            occupancy.append(child.occupancy)
        if len(occupancy) == 4 and all(occupancy):
            self.children = []
            self.occupancy = True
    
    def isOccupied(self, point):
        if self.boundary.contains(point):
            if self.occupancy:
                return True
            else:
                if len(self.children) != 0:
                    occupied = []
                    for child in self.children:
                        occupied.append(child.isOccupied(point))
                    return any(occupied)
                else:
                    return False
    
    def getSize(self):
        if self.children:
            if self.boundary is None:
                return sys.getsizeof(self)
            else:
                sz = 0
                for child in self.children:
                    sz += child.getSize()
                return sz
        else:
            return sys.getsizeof(self.boundary) + sys.getsizeof(self.occupancy)

        
class QuadTree:
    def __init__(self, boundary=None, maxlevel=0):
        self.root = QuadTreeNode(boundary)
        self.maxLevel = maxlevel
    
    def insert(self, data):
        self.root.insert(data, self.maxLevel)
    
    def print_tree(self):
        self.root.print_tree()
    
    def isOccupied(self, point):
        return self.root.isOccupied(point)
    
    def getSize(self):
        return self.root.getSize()

class Tree:
    pad = 100, 100
    center = pad[0]/2, pad[1]/2
    points = []
    def __init__(self, width=100, height=100):
        self._init__pygame()
        self.screen = pygame.display.set_mode((width + self.pad[0], height + self.pad[1]))
        self.clock = pygame.time.Clock()
    
    def _init__pygame(self):
        pygame.init()
        pygame.display.set_caption("QuadTree Map Visualisation")
    
    def draw(self, quadtree):
        self.clearScreen()
        self.drawTree(quadtree)

    def drawTree(self, quadtree):
        w = quadtree.boundary.w
        h = quadtree.boundary.h
        x1 = quadtree.boundary.x + self.center[0]
        y1 = quadtree.boundary.y + self.center[1]
        if quadtree.occupancy:
            pygame.draw.rect(self.screen, GREEN, (x1, y1, w, h))
        pygame.draw.rect(self.screen, BLACK, (x1, y1, w, h), 1)
        if quadtree.children:
            for child in quadtree.children:
                self.drawTree(child)
    
    def draw_point(self, point, memory):
        if memory:
            self.points.append(point)
        else:
            self.points = []    
        for point in self.points:
            x = self.center[0] + point.x
            y = self.center[1] + point.y
            pygame.draw.circle(self.screen, RED, (x, y), 2)

    def drawPCData(self, pcdata):
        if pcdata:
            for point in pcdata.getPoints():
                x = self.center[0] + point.x
                y = self.center[1] + point.y
                pygame.draw.circle(self.screen, RED, (x, y), 2)

    def clearScreen(self):
        self.screen.fill(WHITE)
    
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)
    
    def quit(self):
        pygame.quit()
    
    def eventCheck(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return True

class PointCloud:
    points = []
    pcData = None
    def __init__(self, pcdata):
        self.pcData = pcdata
        self.createPoints()
    
    def createPoints(self):
        if not self.pcData.any():
            return
        for pts in self.pcData:
            self.points.append(Point(pts[0], pts[1]))
    
    def getPoints(self):
        return self.points
    
    def __str__(self):
        string = ""
        for point in self.points:
            string += point.print() + "\n"
            print(point)
        return string