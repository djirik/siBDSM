import split
from genfractal import *
from new_image import encode, save
import random

width = 1000
height = 1000

f = open("test.txt", "rb")
data = f.read()

# Suppose that we have 1000x1000px image

chunk_size = 4*1024 # 4 KB
n_chunks, chunks = split.split("test.txt", chunk_size)


pics = get_images(width, height, n_chunks)
print("number of chunks = ",n_chunks)
n = 0
dic_list= {}
for pic in pics:
    hash = format(random.getrandbits(128), 'x')
    print(hash)
    dic_list.update({n:hash})
    tmp = encode(pic, chunks[n])
    save(tmp,hash,n)
    n += 1
    print(tmp)
print(dic_list)