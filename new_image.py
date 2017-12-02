import struct
import os
from PIL import Image


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


def encode(image: Image.Image, encbytes):
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

    return im


def save(image: Image.Image, image_name, ind):
    if not os.path.exists("tmp"):  # if the dir is not exist
        os.mkdir("tmp")
    elif ind == 0:
        for fname in os.listdir("tmp"):
            os.remove(os.path.join("tmp", fname))
    path = "tmp/" + image_name + ".png"
    image.save(path, "PNG")


def decode(image: Image.Image):
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
    return data
