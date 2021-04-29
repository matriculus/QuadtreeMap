import numpy as np
import tkinter as tk

width = 640
height = 640
level = 6

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Rectangle:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def __str__(self):
        return f"P1: {self.p1}\tP2: {self.p2}"

class Node:
    def __init__(self, boundary, level):
        self.nw = None
        self.sw = None
        self.se = None
        self.ne = None
        self.boundary = boundary
        self.level = level
    
    def __str__(self):
        return f"\nLevel: {self.level}\tBoundary: {self.boundary}\nNW: {self.nw}\nNE: {self.ne}\nSW: {self.sw}\nSE: {self.se}\n"

class Tree:
    level = 0
    def __init__(self, boundary):
        self.primaryNode = self.createNode(boundary, self.level)
        for i in range(level):
            self.primaryNode = self.createNextLevel(self.primaryNode)

    def createNode(self, boundary, level):
        return Node(boundary, level)
    
    def createNextLevel(self, node):
        self.level += 1
        P1 = node.boundary.p1
        P2 = node.boundary.p2
        width = P2[0] - P1[0]
        height = P2[1] - P1[1]
        # nw point
        p1 = P1
        p2 = width/2, height/2
        node.nw = self.createNode(Rectangle(p1,p2), self.level)
        # sw point
        p1 = P1[0], height/2
        p2 = width/2, height
        node.sw = self.createNode(Rectangle(p1, p2), self.level)
        # se point
        p1 = node.nw.boundary.p2
        p2 = P2
        node.se = self.createNode(Rectangle(p1, p2), self.level)
        # ne point
        p1 = width/2, P1[1]
        p2 = P2[0], height/2
        node.ne = self.createNode(Rectangle(p1, p2), self.level)
        return node

class Grid(tk.Tk):
    width = width
    height = height
    geo = str(width) + "x" + str(height)
    def __init__(self):
        tk.Tk.__init__(self)
        self.createWindow()
    
    def createWindow(self):
        self.title("Occupancy Grid")
        self.geometry(self.geo)
    
    def loop(self):
        self.mainloop()


grid = Grid()
grid.loop()

boundary = Rectangle((0,0), (width, height))
tree = Tree(boundary)


print(tree.primaryNode)
