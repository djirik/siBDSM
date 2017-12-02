import split
from genfractal import *
from new_image import encode, save, decode
import random
import os
from AES import *

width = 1024
height = 1024

def enc(file_path):


    # Suppose that we have 1000x1000px image

    # chunk_size = 4*1024 # 4 KB wtf?????? why 4 kb
    n_chunks, chunks = split.split(file_path, int(width * height / 4) - 11)

    # print((width * height / 4) - 11)

    pics = get_images(width, height, n_chunks)
    for each in pics:
        each.save("test.png", "PNG")
    print("number of chunks = ", n_chunks)
    n = 0
    dic_list={}
    for pic in pics:
        img_hash = format(random.getrandbits(128), 'x')
        print(img_hash)
        dic_list.update({n:img_hash})
        tmp = encode(pic, chunks[n])
        save(tmp, img_hash, n)
        n += 1
        print(tmp)
    print(dic_list)


def dec(dir_path, output_file):
    data = b''
    dict_list = {0: '600e8c8feb015c1fb2a8f6f07e53902', 1: '4bb9f4e6724a97289d9a25ce9939f975',
                 2: 'aec57e547be34abaee6a71d7a5a0a09a', 3: '4950fd9068a6b145ba6469cc48d36013',
                 4: '46a7858b1d849934febc7446fe902f41', 5: 'fdd0f2c2a6526051d3dff7664740966f',
                 6: '4491c68ef337a5887e337ab0959be031', 7: '8c66465489f3b69212928ad543497aea',
                 8: '3bc9314ff2babd3d62cb65e243f21b44', 9: '45bea6f2a33eaec468d49f96cece6843',
                 10: '2f59d7a78d6fb1ef6c4b1a1b16d487be', 11: '3889bff1f0a4b6ff83a14b7154b3b838',
                 12: '2b572e9af6eaf5cc55ce21209b88eb61', 13: '838adba4a769012cfdbbbf4a2e72f847',
                 14: '78aa38b7710ec21dc8fd2f16e7c1108', 15: 'cb7430b91f98530b92358a44a3a352fc',
                 16: '783e648c19f1e84cb6b56fbd4b3e5371', 17: '18c931a6e1564e8cba81713bf169d65',
                 18: 'a8711bd8abec28a8ff045be4ed9d83d'}
    dict_key = dict_list.keys()
    for key in dict_key:
        print(dir_path + '/' + dict_list[key] + '.png')
        im = Image.open(dir_path + '/' + dict_list[key] + '.png')
        chunk = decode(im)
        data += chunk
    f = open(output_file, 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':
    #enc('test.mp4')
    dec('tmp', 'decoded.mp4')
