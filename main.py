# import libraries
import numpy as np
import quadtreemap

np.set_printoptions(precision=4)

WIDTH = 640
HEIGHT = WIDTH
maxlevel = 5

Point = quadtreemap.Point
recorder = quadtreemap.Recorder()

boundbox = quadtreemap.Rectangle(0, 0, WIDTH, HEIGHT)
map = quadtreemap.QuadTree(boundbox, maxlevel)
tapp = quadtreemap.Tree(WIDTH, HEIGHT)

def generateCircle(n=300):
    deg = np.random.uniform(0, 360, n)
    ang = deg * np.pi / 180
    r = np.random.uniform(0, 200)
    x = 2.5*WIDTH/4 + r*np.cos(ang)
    y = 2.5*HEIGHT/4 + r*np.sin(ang)
    xy = np.vstack([x, y]).transpose()
    r1 = np.random.uniform(0, 5)
    x1 = 0.7*WIDTH/4 + r1*np.cos(ang)
    y1 = 0.7*HEIGHT/4 + r1*np.sin(ang)
    xy1 = np.vstack([x1, y1]).transpose()
    xy = np.vstack([xy, xy1])
    return quadtreemap.PointCloud(xy)

def generateQuarter(n=300):
    xy = np.random.uniform(0,WIDTH, (n,2))
    return quadtreemap.PointCloud(xy)

# pcData = generateCircle(n=1000)

done = False
while not done:
    pcData = generateCircle(n=10)
    map.insert(pcData)
    tapp.draw(map.root)
    tapp.drawPCData(pcData)
    tapp.update()
    recorder.save(tapp.screen)
    done = tapp.eventCheck()
    del pcData

map.print_tree()