import os, imageio

png_dir = "Snaps"
images = []
for file in sorted(os.listdir(png_dir)):
    fpath = os.path.join(png_dir, file)
    images.append(imageio.imread(fpath))

imageio.mimsave("quadtree.gif", images)