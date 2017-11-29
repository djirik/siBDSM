import image
import join
import imgen
import math
import split
import random

width = 1000
height = 1000

f = open("Test.mp3", "rb")
data = f.read()

# Suppose that we have 1000x1000px image
pics = []

n_pics, pics = split.split("Test.mp3", ".", width * height)


for i in range(1, n_pics):
    pics.append(imgen.get_image(height, width))


