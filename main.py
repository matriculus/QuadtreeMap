# import libraries
import random
import quadtreemap
import math

WIDTH = 640
HEIGHT = WIDTH
maxlevel = 5

Point = quadtreemap.Point

boundbox = quadtreemap.Rectangle(0, 0, WIDTH, HEIGHT)
map = quadtreemap.QuadTree(boundbox, maxlevel)
tapp = quadtreemap.Tree(WIDTH, HEIGHT)
done = False
while not done:
    deg = random.randrange(360)
    ang = (math.pi * deg)/180
    x = WIDTH/2 + 200*math.cos(ang)
    y = HEIGHT/2 + 200*math.sin(ang)
    p = Point(x, y)
    map.insert(p)
    tapp.draw(map.root)
    tapp.draw_point(p, False)
    tapp.update()
    done = tapp.eventCheck()

map.print_tree()