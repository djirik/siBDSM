"""This file includes functionality to merge data with PNG file."""

import struct


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
