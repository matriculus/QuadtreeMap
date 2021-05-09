# import libraries
import numpy as np
import quadtreemap
import sys

WIDTH = 640
HEIGHT = WIDTH
maxlevel = 5

Point = quadtreemap.Point

boundbox = quadtreemap.Rectangle(0, 0, WIDTH, HEIGHT)
map = quadtreemap.QuadTree(boundbox, maxlevel)

tapp = quadtreemap.Tree(WIDTH, HEIGHT)
done = False
while not done:
    deg = np.random.randint(360, size=(50))
    ang = (np.pi * deg)/180
    x = WIDTH/2 + np.random.randint(100,200)*np.cos(ang)
    y = HEIGHT/2 + np.random.randint(100,200)*np.sin(ang)
    p = quadtreemap.PointCloud(np.vstack([x,y]).transpose())
    map.insert(p)
    # print(f"Occupied?: {map.isOccupied(Point(x + 50, y + 50))}")
    tapp.draw(map.root)
    # tapp.draw_point(p, False)
    tapp.update()
    done = tapp.eventCheck()

map.print_tree()

print(map.getSize())

xx = 2**maxlevel
yy = 2**maxlevel
print(sys.getsizeof(1)*xx*yy)