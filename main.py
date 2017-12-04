import split
from genfractal import *
from new_image import encode, save, decode
import random
import pickle
from encryption import enc, dec
import ast
import os
import time

width = 1024
height = 1024
cluch = b'lolololololololo'


def encode_file(file_path):
    n_chunks, chunks = split.split(file_path, int(width * height / 4) - 43)

    dic_list = {}
    pics = get_images(width, height, n_chunks)

    enc_data = enc(chunks, cluch,n_chunks)  # encryption)
    tmp = encode(pics, enc_data)

    img_hash=[]
    for n in range(n_chunks):
        single_hash = format(random.getrandbits(128), 'x')
        img_hash.append(single_hash)
        dic_list.update({n: single_hash})
    save(tmp, img_hash)

    img_hash.clear()
    img_hash.append(format(random.getrandbits(128), 'x'))
    enc_dict = enc(str(dic_list).encode(), cluch,1)
    master_image = get_images(width, height)
    tmp = encode(master_image, enc_dict)
    save(tmp,img_hash, 1)



def decode_file(dir_path, output_file):
    maxim = 0
    res = ''
    for each in os.listdir(dir_path):
        if os.path.getmtime(dir_path + '/' + each) > maxim:
            maxim = os.path.getmtime(dir_path + '/' + each)
            res = each
    f = Image.open(dir_path + '/' + res)

    image_list=[]
    image_list.append(f)
    dict_list = decode(image_list)
    dict_list = ast.literal_eval(dec(dict_list, cluch)[0].decode())

    dict_key = dict_list.keys()
    image_list = []
    for key in dict_key:
        im = Image.open(dir_path + '/' + dict_list[key] + '.png')
        image_list.append(im)

    chunk = decode(image_list)
    dec_data = dec(chunk, cluch)  # decryption
    data=b''
    for x in range(len(dec_data)):
        data += dec_data[x]
    f = open(output_file, 'wb')
    f.write(data)
    f.close()

if __name__ == '__main__':
    start = time.time()
    encode_file('test.mp4')
    decode_file('tmp', 'decoded.mp4')
    elapsed = time.time() - start
    print(elapsed)