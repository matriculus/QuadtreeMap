# import libraries
import numpy as np
import quadtreemap
import math

np.set_printoptions(precision=4)

WIDTH = 640
HEIGHT = WIDTH
maxlevel = 5

Point = quadtreemap.Point

boundbox = quadtreemap.Rectangle(0, 0, WIDTH, HEIGHT)
map = quadtreemap.QuadTree(boundbox, maxlevel)
tapp = quadtreemap.Tree(WIDTH, HEIGHT)

deg = np.random.uniform(0, 360, 300)
ang = deg * np.pi / 180

x = WIDTH/2 + 200*np.cos(ang)
y = HEIGHT/2 + 200*np.sin(ang)
xy = np.vstack([x, y]).transpose()

pcData = quadtreemap.PointCloud(xy)
# print(pcData)
print(pcData)

p = Point(x[0], y[0])
map.insert(pcData)

done = False
while not done:
    tapp.draw(map.root)
    tapp.drawPCData(pcData)
    tapp.update()
    done = tapp.eventCheck()

map.print_tree()