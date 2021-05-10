import pygame
import sys
import copy

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
        self.parent = None
        self.occupancy = False
        self.children = {}
    
    def addChild(self, child=None, label="NW"):
        child.parent = self
        self.children[label] = child
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def containsChildren(self):
        return any(self.children.values())

    def print_tree(self):
        prefix = f"{self.get_level()} "
        spacer = ' ' * self.get_level()*3 + "|____" if self.parent else ""
        statement = prefix + spacer + f"{self.boundary}" + f"\tOccupied: {self.occupancy}"
        print(statement)
        if self.containsChildren():
            for child in self.children.values():
                child.print_tree()
    
    def add_level(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        # nw point
        self.addChild(QuadTreeNode(Rectangle(x, y, w/2, h/2)), "NW")
        # sw point
        self.addChild(QuadTreeNode(Rectangle(x, y + h/2, w/2, h/2)), "SW")
        # se point
        self.addChild(QuadTreeNode(Rectangle(x + w/2, y + h/2, w/2, h/2)), "SE")
        # ne point
        self.addChild(QuadTreeNode(Rectangle(x + w/2, y, w/2, h/2)), "NE")
    
    def add_until_level(self, maxLevel):
        if maxLevel <= self.get_level() : return
        self.add_level()
        for child in self.children.values(): child.add_until_level(maxLevel)
    
    def insertPoint(self, point, maxLevel):
        if not self.boundary.contains(point):
            return
        
        if maxLevel <= self.get_level():
            if self.boundary.contains(point):
                self.occupancy = True
            return
        
        if (not self.containsChildren()):
            if (not self.occupancy):
                self.add_level()
            else:
                return
        for child in self.children.values():
            child.insertPoint(point, maxLevel)
    
    def insertPCData(self, pcData, maxLevel):
        if pcData:
            for point in pcData.getPoints():
                self.insertPoint(point, maxLevel)
    
    def insert(self, data, maxLevel):
        if isinstance(data, Point):
            self.insertPoint(data, maxLevel)
        elif isinstance(data, PointCloud):
            self.insertPCData(data, maxLevel)

    def mergeOccupiedNodes(self):
        occupancy = []
        if not self.containsChildren():
            return
        for child in self.children.values():
            child.mergeOccupiedNodes()
            occupancy.append(child.occupancy)
        if len(occupancy) == 4 and all(occupancy):
            self.children = {}
            self.occupancy = True
    
    def mergeFreeNodes(self):
        if not self.containsChildren():
            return
        occupancy = []
        for child in self.children.values():
            child.mergeFreeNodes()
            occupancy.append(child.occupancy)
        if len(occupancy) == 4 and (not any(occupancy)) :
            self.children = {}
            self.occupancy = False
    
    def isOccupied(self, point):
        if self.boundary.contains(point):
            if self.occupancy:
                return True
            else:
                if self.containsChildren():
                    occupied = False
                    for child in self.children.values():
                        occupied = occupied or child.isOccupied(point)
                    return occupied
                else:
                    return False
    
    def getSize(self):
        if self.containsChildren():
            if self.boundary is None:
                return sys.getsizeof(self)
            else:
                sz = 0
                for child in self.children.values():
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
        self.root.mergeOccupiedNodes()
    
    def print_tree(self):
        self.root.print_tree()
        print(f"Size: {self.getSize()}")
    
    def isOccupied(self, point):
        return self.root.isOccupied(point)
    
    def getSize(self):
        return self.root.getSize()
    
    def invertTree(self, tree):
        if tree.containsChildren():
            keys = []
            for key, child in tree.children.items():
                if child.occupancy: keys.append(key)
                else: self.invertTree(child)
            for key in keys: tree.children.pop(key)

        else: return

    def invert(self):
        qtree = copy.copy(self)
        self.invertTree(qtree.root)
        # qtree.root.mergeFreeNodes()
        return qtree

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
        if quadtree.containsChildren():
            for child in quadtree.children.values():
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