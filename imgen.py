from PIL import Image
import os


def get_image(height, width):
    size = (height, width)
    im = Image.new('RGB', size)

    def ran():
        return os.urandom(height*width)

    pixels = zip(ran(), ran(), ran())
    im.putdata(list(pixels))

    return im
