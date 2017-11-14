from PIL import Image
import os
size = (1000, 1000)
im = Image.new('RGB', size)
def ran():
    return os.urandom(1000*1000) 
pixels = zip(ran(), ran(), ran())
im.putdata(list(pixels))
im.save("imagedone.png")

#im.show()