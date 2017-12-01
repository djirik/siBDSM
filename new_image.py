import struct
from PIL import  Image

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
    a = (byte & 192) >> 6

    color = (
             pixel[0],
             pixel[1],
             pixel[2],
             a + (pixel[3] & 252)
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

    result = a << 6
    return struct.pack("B", result)


def encode(image: Image.Image, encbytes):
    im = image
    px = im.load()

    header = Header()
    header.size = len(encbytes)

    header_data = struct.pack('4sI' + str(len(header.fformat)) + 's', header.magicnum,  header.size, header.fformat)

    data = header_data + encbytes

    for i in range(len(data)):
        if i == 999:
            print(i)
        for
        coords = (i % im.width, int(i / im.width))
        tmp = data[i]
        # byte = ord(tmp)

        px[coords[0], coords[1]] = encode_in_pixel(tmp, px[coords[0], coords[1]])

    return im


def save(image: Image.Image, path='output.png'):
    image.save(path, "PNG")


def decode(image: Image.Image):
    pass