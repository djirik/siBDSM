import split
from genfractal import *
from new_image import encode, save

width = 1000
height = 1000

f = open("test.txt", "rb")
data = f.read()

# Suppose that we have 1000x1000px image


n_chunks, chunks = split.split("test.txt", width * height)


pics = get_images(width, height, n_chunks)

n = 0

for pic in pics:

    tmp = encode(pic, chunks[n])
    save(tmp)
    n += 1
    print(tmp)
