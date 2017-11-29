"""This file includes functionality to merge data with PNG file."""

import struct
from PIL import Image
import os


class Header:
    MAX_FORMAT_LENGTH = 8
    magicnum = "hide"
    size = 0
    fformat = "txt"


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


def encode(image_file, filename):
    im = Image.open(image_file)
    px = im.load()

    f = open(filename, "rb")
    data = f.read()
    # Create a header
    header = Header()
    header.size = len(data)
    header.fformat = "" if (len(filename.split(os.extsep)) < 2) else filename.split(os.extsep)[1]

    # Add the header to the file data
    header_data = struct.pack("4s" +
                             "I" +
                             str(Header.MAX_FORMAT_LENGTH)+"s",
                             header.magicnum, header.size, header.fformat)
    filebytes = header_data + data

    if len(filebytes) > im.width * im.height:
        print("Image too small to encode the file. \
      You can store 1 byte per pixel.")
        exit()

    for i in range(len(filebytes)):
        coords = (i % im.width, i / im.width)

        byte = ord(filebytes[i])

        px[coords[0], coords[1]] = encode_in_pixel(byte, px[coords[0], coords[1]])

    im.save("output.png", "PNG")

    return im


def decode(image):
    im = Image.open(image)
    px = im.load()

    data = ""

    # Decode the contents of the hidden data
    for i in range(im.height):
        for j in range(im.width):
            data += decode_from_pixel(px[j, i])

    # Create the header for reading
    header = Header()

    headerdata = struct.unpack("4s" +
                               "I" +
                               str(Header.MAX_FORMAT_LENGTH)+"s",
                                data[:4+4+Header.MAX_FORMAT_LENGTH])

    header.magicnum = headerdata[0]
    header.size = headerdata[1]
    header.fformat = headerdata[2].strip("\x00")

    # Verify integrity of recovered data
    if header.magicnum != Header.magicnum:
        print("There is no data to recover, quitting")
        exit()

    data = data[4+Header.MAX_FORMAT_LENGTH:4+Header.MAX_FORMAT_LENGTH+header.size]

    print("Saving decoded output as {}".format("output"+os.extsep+header.fformat))
    with open("output"+os.extsep+header.fformat, 'wb') as outf:
        outf.write(data)


def save_image(image, filename):
    image.save(filename, "PNG")


def encode_and_save(image: Image, data_file: str, save_file: str):
    save_image(encode(image, data_file), save_file)
