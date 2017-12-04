import struct
import os
from PIL import Image
import multiprocessing

class Header:
    MAX_FORMAT_LENGTH = 8
    magicnum = b"hide"
    size = 0
    fformat = b"txt"


def encode_in_pixel(byte, pixel):
    """Encodes a byte in the two least significant bits of each channel.
    A 4-channel pixel is needed, which should be a tuple of 4 values from 0 to
    255.
    """
    # r = (byte & 3)
    # g = (byte & 12) >> 2
    # b = (byte & 48) >> 4
    a = (byte & 3)
    tmp = a + (pixel[3] & 252)

    color = (
             pixel[0],
             pixel[1],
             pixel[2],
             tmp
            )
    return color


def decode_from_pixel(pixel):
    """Retrieves an encoded byte from the pixel.
    The pixel should be a tuple of 4 values from 0 to 255.
    """
    # r = pixel[0] & 3
    # g = pixel[1] & 3
    # b = pixel[2] & 3
    a = pixel[3] & 3

    result = a
    tmp = struct.pack("B", result)
    return result


def encode_fun(image , encbytes,enc_data_list=[],x=0):
    im = image
    px = im.load()

    header = Header()
    header.size = len(encbytes)

    header_data = struct.pack('4sI' + str(len(header.fformat)) + 's', header.magicnum,  header.size, header.fformat)
    # print(len(header_data))
    data = header_data + encbytes

    for i in range(len(data)):

        for j in range(4):
            coords = ((4 * i + j) % im.width, int((4 * i + j) / im.width))
            tmp = data[i] >> (j * 2)
        # byte = ord(tmp)

            px[coords[0], coords[1]] = encode_in_pixel(tmp, px[coords[0], coords[1]])

    enc_data_list[x] = im

def encode(images, enc_data):
    manager= multiprocessing.Manager()
    jobs=[]
    enc_data_list = manager.list(range(len(images)))
    for x in range(len(images)):
        p = multiprocessing.Process(target=encode_fun, args=(images[x],enc_data[x],enc_data_list,x))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return enc_data_list


def save_fun(image, image_name):
    path = "tmp/" + image_name + ".png"
    image.save(path, "PNG")

def save(image, img_hash, ind=0):
    if not os.path.exists("tmp"):  # if the dir is not exist
        os.mkdir("tmp")

    jobs=[]
    for x in range(len(image)):
        if ind == 0:
            for fname in os.listdir("tmp"):
                os.remove(os.path.join("tmp", fname))
        ind=1
        p = multiprocessing.Process(target=save_fun, args=(image[x], img_hash[x]))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
def decode_fun(image,dec_data_list,x):
    #im = Image.open(image)
    px = image.load()

    data = b""

    # Decode the contents of the hidden data
    for i in range(image.height):
        for j in range(0, image.width, 4):
            # print(px[j, i])
            pair0 = decode_from_pixel(px[j, i])
            pair1 = decode_from_pixel(px[j + 1, i]) << 2
            pair2 = decode_from_pixel(px[j + 2, i]) << 4
            pair3 = decode_from_pixel(px[j + 3, i]) << 6

            tmp = pair0 + pair1 + pair2 + pair3

            # print(j % 4)

            data += tmp.to_bytes(1, byteorder="big")

    # Create the header for reading
    header = Header()

    headerdata = struct.unpack("4s" +
                               "I" +
                               str(Header.MAX_FORMAT_LENGTH) + "s",
                               data[:4 + 4 + Header.MAX_FORMAT_LENGTH])

    header.magicnum = headerdata[0]
    header.size = headerdata[1]
    header.fformat = headerdata[2].strip(b"\x00")

    data = data[3 + Header.MAX_FORMAT_LENGTH:3 + Header.MAX_FORMAT_LENGTH + header.size]
    # print(data)
    dec_data_list[x] = data

def decode(images):
    manager= multiprocessing.Manager()
    jobs=[]
    dec_data_list = manager.list(range(len(images)))
    for x in range(len(images)):
        p = multiprocessing.Process(target=decode_fun, args=(images[x],dec_data_list,x))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return dec_data_list