from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import  multiprocessing
# key = get_random_bytes(16)


def enc_fun(input_data, key=b'',enc_data_list=[],x=0):
    i_vec = b'1234567812345678'
    encryptor = AES.new(key, AES.MODE_CBC, i_vec)
    if type(input_data) is list:
        enc_data_list[x] = encryptor.encrypt(pad(input_data[x], 32))
    else:
        enc_data_list[x] = (encryptor.encrypt(pad(input_data, 32)))
    # print(enc_data)

def enc(input_data, key,len):
    manager= multiprocessing.Manager()
    jobs=[]
    enc_data_list = manager.list(range(len))
    for x in range(len):
        p = multiprocessing.Process(target=enc_fun, args=(input_data, key,enc_data_list,x))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return enc_data_list


def dec_fun(enc_data, key,dec_data_list,x):
    i_vec = b'1234567812345678'
    encryptor = AES.new(key, AES.MODE_CBC, i_vec)
    dec_data_list[x] = unpad(encryptor.decrypt(enc_data[x]), 32)


def dec(input_data, key):
    manager= multiprocessing.Manager()
    jobs=[]
    dec_data_list = manager.list(range(len(input_data)))
    for x in range(len(input_data)):
        p = multiprocessing.Process(target=dec_fun, args=(input_data, key,dec_data_list,x))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return dec_data_list