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

    # print((width * height / 4) - 11)

    pics = get_images(width, height, n_chunks)
    dic_list = {}
    master_name = int('308b8f9420f13dccd58b0b761e6b4a11', 16)

    for i in range(n_chunks):
        img_hash = format(random.getrandbits(128), 'x')
        master_name = master_name ^ int(img_hash, 16)
        dic_list.update({i: img_hash})


    n = 0

    for pic in pics:
        enc_data = enc(chunks[n], cluch)  # encryption

        tmp = encode(pic, enc_data)

        save(tmp, dic_list[n], n)
        n += 1

    enc_dict = enc(str(dic_list).encode(), cluch)
    master_image = get_images(width, height)[0]

    tmp = encode(master_image, enc_dict)
    print(format(master_name, 'x'))
    save(tmp, format(master_name, 'x'), 1)

    print("number of chunks = ", n_chunks)


    pickle.dump(dic_list, open('dic.img', 'wb'))


def decode_file(dir_path, output_file):
    data = b''
    # dict_list = pickle.load(open('dic.img', 'rb'))
    # f = Image.open('tmp/111111.png')
    maxim = 0
    res = ''
    for each in os.listdir(dir_path):
        if os.path.getmtime(dir_path + '/' + each) > maxim:
            maxim = os.path.getmtime(dir_path + '/' + each)
            res = each
    print(res)

    f = Image.open(dir_path + '/' + res)

    dict_list = decode(f)
    dict_list = ast.literal_eval(dec(dict_list, cluch).decode())
    print(dict_list)
    dict_key = dict_list.keys()
    for key in dict_key:
        # print(dir_path + '/' + dict_list[key] + '.png')
        im = Image.open(dir_path + '/' + dict_list[key] + '.png')
        chunk = decode(im)
        dec_data = dec(chunk, cluch)  # decryption
        data += dec_data
    f = open(output_file, 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':
    start = time.time()
    encode_file('test.mp4')
    decode_file('tmp', 'decoded.mp4')
    elapsed = time.time() - start
    print(elapsed)
