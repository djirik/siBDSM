"""This file includes functionality to merge data with PNG file."""

import struct
from PIL import Image
import os

def encode_in_pixel(byte, pixel):
    """Encodes a byte in the two least significant bits of each channel.
    A 4-channel pixel is needed, which should be a tuple of 4 values from 0 to
    255.
    """
    r = (byte & 3)
    g = (byte & 12) >> 2
    b = (byte & 48) >> 4
    a = (byte & 192) >> 6

    color = (r+(pixel[0] & 252),
             g+(pixel[1] & 252),
             b+(pixel[2] & 252),
             a+(pixel[3] & 252))
    return color


class Header:
    MAX_FORMAT_LENGTH=8
    magicnum = "hide"
    size = 0
    fformat = "txt"


def decode_from_pixel(pixel):
    """Retrieves an encoded byte from the pixel.
    The pixel should be a tuple of 4 values from 0 to 255.
    """
    r = pixel[0] & 3
    g = pixel[1] & 3
    b = pixel[2] & 3
    a = pixel[3] & 3

    result = r + (g << 2) + (b << 4) + (a <<6)
    return struct.pack("B", result)


def encode(image, data, filename, encryption=False, password=""):
    im = Image.open(image)
    px = im.load()

    # Create a header
    header = Header()
    header.size = len(data)
    header.fformat = "" if (len(filename.split(os.extsep))<2)\
                     else filename.split(os.extsep)[1]

    # Add the header to the file data
    header_data = struct.pack("4s" +
                             "I" +
                             str(Header.MAX_FORMAT_LENGTH)+"s",\
                             header.magicnum, header.size, header.fformat)
    filebytes = header_data + data
