from PIL import Image
import random
from multiprocessing.pool import ThreadPool
from threading import Thread

# image size
def get_image(result, index ,imgx=512, imgy=512):
    # imgx = 512
    # imgy = 512

    im = Image.new("RGBA", (imgx, imgy))
    #im_as_array = np.zeros((imgy, imgx), dtype=(b))

    # drawing area
    xa = -2.0
    xb = 2.0
    ya = -1.5
    yb = 1.5
    maxIt = 255 # max iterations allowed
    rand1 = random.choice([8,16,32])
    rand2 = random.choice([8,16,32])
    rand3 = random.choice([8,16,32])
    # find a good Julia set point using the Mandelbrot set
    while True:
        cx = random.random() * (xb - xa) + xa
        cy = random.random() * (yb - ya) + ya
        c = cx + cy * 1j
        z = c
        for i in range(maxIt):
            if abs(z) > 2.0:
                break 
            z = z * z + c
        if i > 10 and i < 100:
            break

    # draw the Julia set
    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1)  + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1)  + xa
            z = zx + zy * 1j
            for i in range(maxIt):
                if abs(z) > 2.0:
                    break 
                z = z * z + c
            im.putpixel((x, y), (i % rand1 * 32, i % rand2 * 32, i % rand3 * 32, 255))
            #im_as_array
            result[index] = im
    return im
    #im.save("juliaFr.png", "PNG")


def get_images(width=512, height=512, amount=1) -> [Image.Image]:
    images = [Image.Image] * amount

    threads = [None] * amount


    for i in range(amount):
        threads[i] = Thread(target=get_image, args=(images, i, width, height))
        threads[i].start()

    for i in range(amount):
        threads[i].join()
    print(images)
    return images
