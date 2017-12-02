from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# key = get_random_bytes(16)


def enc(input_data: bytes, key: bytes) -> bytes:
    i_vec = b'1234567812345678'
    encryptor = AES.new(key, AES.MODE_CBC, i_vec)

    enc_data = encryptor.encrypt(pad(input_data, 32))
    # print(enc_data)
    return enc_data


def dec(enc_data: bytes, key: bytes) -> bytes:
    i_vec = b'1234567812345678'
    encryptor = AES.new(key, AES.MODE_CBC, i_vec)

    data = unpad(encryptor.decrypt(enc_data), 32)
    # print(data)
    return data

# test = b'dsfa khgfh ghfbhdsagfh usadfh jnsdaf ndsafds dsf gdsgdfrweqwew qwe'
#
# tmp = enc(test, b'lolololololololo')
#
# dec(tmp, b'lolololololololo')


