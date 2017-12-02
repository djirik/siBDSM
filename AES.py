import os, random, struct
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    IV = b'1234567812345678'
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            # outfile.write(struct.pack('<Q', filesize))
            # outfile.write(IV)
            outfile = struct.pack('<Q', filesize)
            outfile = IV
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += bytes(' ' * (16 - len(chunk) % 16), encoding="utf8")

                outfile = encryptor.encrypt(chunk)
                # enc_file = outfile.write(encryptor.encrypt(chunk))
    # print(outfile)
    return chunk


# encrypt_file(key, 'julianumba.png')

def decrypt_file(key, enc_bytes, out_filename, chunksize=24 * 1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be enc_file without its last extension
        (i.e. if enc_file is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(enc_bytes)[0]

    origsize = struct.unpack('<Q', enc_bytes.read(struct.calcsize('Q')))[0]
    iv = enc_bytes.read(16)
    decryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(out_filename, 'wb') as outfile:
        while True:
            chunk = enc_bytes.read(chunksize)
            if len(chunk) == 0:
                break
            outfile = decryptor.decrypt(chunk)
        outfile.truncate(origsize)

    return outfile