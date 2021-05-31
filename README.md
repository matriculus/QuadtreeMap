# QuadtreeMap
Quadtree is a tree where a parent node contains exactly 4 child nodes and they represent any grid.
This Quadtree structure shows how the point cloud data can be converted into an occupancy grid map without dealing with matrices.

As size of objects are smaller, the regular matrix grid becomes extremely large to maintain (O(n^3)). Same time any big obstacle contains a lot of grids marked as occupied. Searching for free space or inside a grid is expensive.

Quadtree solves the issue but creating nodes when necessary and merging nodes is all the child nodes are occupied. So both small and large objects can be represented in a very effective manner in grid without blowing up memory.

Here is an example of point data from a circular object being represented in a single map with quadtree.
[QuadTree Map](quadtree.gif)