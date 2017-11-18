from numpy import *
from pylab import *
import time
import sys

def julia(n, m, itermax, xmin, xmax, ymin, ymax, name):
    """
    Fast julia computation.
    n, m - size of the output image
    itermax - the maximum iterations number
    xmin, xmax, ymin, ymax specify the region of the
    set to compute.
    """
    ix, iy = mgrid[0:n, 0:m]  # The points of 2D arrays giving the x-coord and y-coord at each point in the array
    x = linspace(xmin, xmax, n)[ix]  #linspace(start, end, n) 
    y = linspace(ymin, ymax, m)[iy]
    z = x + complex(0, 1) * y  # z is the complex number with the given x, y coords
    del x, y 
    # c = random(1)*1.2 - .5 + complex(0,1)*(random(1)*1.-.5)
    r = 0.8 + random(1) / 5
    phi = random(1)*2*pi
    c = r*cos(phi) + complex(0, 1) * r * sin(phi)
    img = zeros(z.shape, dtype=int)
    ix.shape = n*m
    iy.shape = n*m
    z.shape = n*m
    PARS = random(3) / 2
    for i in range(itermax):
        if not len(z):
            break
        if random(1) < PARS[0]:
            z = log(z)
        if random(1) < PARS[1]:
            multiply(z, z, z)
        if random(1) < 0.5:
            z = 1 / (complex(1, 1)-z)
        else :
            multiply(z, z, z)
        if random(1) < PARS[2] :
            add(z, c, z)
        else :
            add(z, -c, z)
            
        rem = abs(z) > 2.0
        img[ix[rem], iy[rem]] = i+1
        rem = ~rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
        # c = c[rem]
        timg = log(img+1)
        #timg[timg==0] = 101
        if( i > 10 ):
            continue
        ttimg = imshow(timg.T, origin='lower left')
        ttimg.write_png(name+'_'+str(i)+'.png')
        # ttimg.write_png(name+'_'+str(i)+'.png', noscale=True)
    return ttimg
 
if __name__=='__main__':

    if( len(sys.argv) > 1 ):
        name = str(sys.argv[1])
    else:
        name = 'fc'
    for ITER in range(0, 1):
        # print ITER
        # start = time.time()
        I = julia(800, 800, 100, -2, 2, -2, 2, name)  
        # print 'Time taken:', time.time()-start
        I[I == 0] = 101
        img = imshow(I.T, origin='lower left')
        img.write_png(name+'.png')
        del I, img
