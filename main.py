# import libraries
import random
import quadtreemap

WIDTH = 640
HEIGHT = WIDTH
maxlevel = 10

Point = quadtreemap.Point

boundbox = quadtreemap.Rectangle(0, 0, WIDTH, HEIGHT)
map = quadtreemap.QuadTree(boundbox, maxlevel)
app = quadtreemap.Tree(WIDTH, HEIGHT)
points = []
for _ in range(500):
    x = random.randrange(WIDTH)
    y = random.randrange(HEIGHT)
    points.append(Point(x, y))
    map.insert(Point(x, y))

map.print_tree()

app.draw(map.root)
for p in points:
    app.draw_point(p)
app.loop()