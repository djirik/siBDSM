import split
from genfractal import *
from new_image import encode, save, decode
import random


width = 1000
height = 1000

# f = open("test.txt", "rb")
# data = f.read()
#
# # Suppose that we have 1000x1000px image
#
# # chunk_size = 4*1024 # 4 KB wtf?????? why 4 kb
# n_chunks, chunks = split.split("test.txt", int(width * height / 4))
#
#
# pics = get_images(width, height, n_chunks)
# for each in pics:
#     each.save("test.png", "PNG")
# print("number of chunks = ", n_chunks)
# n = 0
# dic_list= {}
# for pic in pics:
#     hash = format(random.getrandbits(128), 'x')
#     print(hash)
#     dic_list.update({n:hash})
#     tmp = encode(pic, chunks[n])
#     save(tmp, hash, n)
#     n += 1
#     print(tmp)
# print(dic_list)


im = Image.open('''8a9a2acf451c89ec0fa1d9e4fa25262c.png''')

decode(im)
