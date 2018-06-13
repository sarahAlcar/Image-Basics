import argparse 
from scipy import misc, stats, math
from PIL import Image
import numpy as np
from skimage import feature, io

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def nn_interpolation (x, y, img):
    point = 0
    dx = x - math.floor(x)
    dy = y - math.floor(y)

    ix = int(math.floor(x))
    iy = int(math.floor(y))

    if (dx < 0.5 and dy < 0.5):
        point = img[iy,ix]
    elif ((dx >= 0.5 and dy < 0.5) and ((x+1 >= 0 and x+1 <img.shape[1]) and (y >= 0 and y <img.shape[0]))):
        point = img[iy,ix+1]
    elif ((dx < 0.5 and dy >= 0.5) and ((x >= 0 and x <img.shape[1]) and (y+1 >= 0 and y+1 <img.shape[0]))):
        point = img[iy+1,ix]
    elif ((dx >= 0.5 and dy >= 0.5) and ((x+1 >= 0 and x+1 <img.shape[1]) and (y+1 >= 0 and y+1 <img.shape[0]))):
        point = img[iy+1,ix+1]
        
    return point
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def bilinear_interpolation (x, y,img):
    ix = int(math.floor(x))
    iy = int(math.floor(y))

    dx = x - math.floor(x)
    dy = y - math.floor(y)
    point = 0
    if ((x >= 0 and x <img.shape[1]) and (y >= 0 and y <img.shape[0])):
        point = ((1-dx)*(1-dy)*img[iy, ix]) 
    if ((x+1 >= 0 and x+1 <img.shape[1]) and (y >= 0 and y <img.shape[0])):
        point = point + (dx*(1-dy)*img[iy, ix+1]) 
    if ((x >= 0 and x <img.shape[1]) and (y+1 >= 0 and y+1 <img.shape[0])):
        point = point + ((1-dx)*dy*img[iy+1, ix]) 
    if ((x+1 >= 0 and x+1 <img.shape[1]) and (y+1 >= 0 and y+1 <img.shape[0])):
        point = point + (dx*dy*img[iy+1,ix+1]) 
    return point
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def P(index2):
    if (index2 > 0):
        index2 = index2
    elif (index2 <= 0):
        index2 = 0
    return index2
    
def R(index):
    r = ((P(index+2)**3)-4*(P(index+1)**3)+6*(P(index)**3)-4*(P(index-1)**3))/6
    return r

def bicubic_interpolation (x, y, img):
    ix = int(math.floor(x))
    iy = int(math.floor(y))

    dx = x - math.floor(x)
    dy = y - math.floor(y)
    temp = 0
    for m in range(-1, 3):
        for n in range(-1, 3): 
            if ((x+m >= 0 and x+m <img.shape[1]) and (y+n >= 0 and y+n <img.shape[0])):           
                temp = temp + img[iy+n, ix+m]*R(m-dx)*R(dy-n)
    point = temp
    return point


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def L(n, dx, img, x, y):
    l = 0

    ix = int(math.floor(x))
    iy = int(math.floor(y))
    

    if ((x+1 >= 0 and x+1 <img.shape[1]) and (y+n-2 >= 0 and y+n-2 <img.shape[0])): 
        l = ((-dx*(dx-1)*(dx-2)*img[iy+n-2, ix+1])/6)
    if ((x >= 0 and x <img.shape[1]) and (y+n-2 >= 0 and y+n-2 <img.shape[0])): 
        l = l+(((dx+1)*(dx-1)*(dx-2)*img[iy+n-2,ix])/2)
    if ((x+1 >= 0 and x+1 <img.shape[1]) and (y+n-2 >= 0 and y+n-2 <img.shape[0])):
        l = l+((-dx*(dx+1)*(dx-2)*img[iy+n-2,ix+1])/2)
    if ((x+2 >= 0 and x+2 <img.shape[1]) and (y+n-2 >= 0 and y+n-2 <img.shape[0])):
        l = l+((dx*(dx+1)*(dx-1)*img[iy+n-2, ix+2])/6)
    return l

def lagrange_interpolation (x, y, img):

    dx = x - math.floor(x)
    dy = y - math.floor(y)
    L1 = L(1, dx, img, x, y)
    L2 = L(2, dx, img, x, y)
    L3 = L(3, dx, img, x, y)
    L4 = L(4, dx, img, x, y)
    point = ((-dy*(dy-1)*(dy-2)*L1)/6)+(((dy+1)*(dy-1)*(dy-2)*L2)/2)+((-dy*(dy+1)*(dy-2)*L3)/2)+((dy*(dy+1)*(dy-1)*L4)/6)
    return point
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def interpolate (y, x, img, method):
    if (method == 1 ):
        # print "1"
        value = nn_interpolation (x, y, img)
    elif (method == 2 ):
        # print "2"
        value = bilinear_interpolation (x, y, img)
    elif (method == 3 ):
        # print "3"
        value = bicubic_interpolation (x, y, img)
    elif (method == 4 ):
        # print "4"
        value = lagrange_interpolation (x, y, img)
    return value
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def rotation(img, angle, method):
    x0 = round(img.shape[1]/2)
    y0 = round(img.shape[0]/2)
    img1 = np.zeros(shape=img.shape)
    for yn in range (img1.shape[0]):
        for xn in range (img1.shape[1]):
            x = math.cos(math.radians(-angle))*(xn-x0) - math.sin(math.radians(-angle))*(yn-y0)+x0
            y = math.sin(math.radians(-angle))*(xn-x0) + math.cos(math.radians(-angle))*(yn-y0)+y0
            img1 [yn, xn] = interpolate(y, x, img, method)
    return img1

def scaleD (img, wf, hf, method):
    wo =  img.shape[0]
    ho =  img.shape[1]
    nfacW = wf/float(wo)
    nfacH = hf/float(ho)
    img1 = scale (img, nfacW, nfacH, method)
    return img1

def scaleS (img, factor, method):
    img1 = scale (img, factor, factor, method)
    return img1

def scale(img, wf, hf, method):  
    img1 = np.zeros(shape=(int(img.shape[0]*hf),int(img.shape[0]*wf)))  
    for yn in range (img1.shape[0]):
        for xn in range (img1.shape[1]):
            x = xn/float(wf)
            y = yn/float(hf)
            img1 [yn, xn] = interpolate(y, x, img, method)
    return img1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def main ( ):
    a = argparse.ArgumentParser ( )
    a.add_argument ('-a', type = float, nargs =1, help = "Rotation angle")
    a.add_argument ('-e', type = float, nargs =1, help = "Scale factor")
    a.add_argument ('-d', type = int, nargs =2, help = "Width and height")
    a.add_argument ('-m', type = int, nargs =1, help = "Interpolation method", default=1)
    a.add_argument ('-i', type = str,nargs =1, help = "Input name")
    a.add_argument ('-o', type = str, nargs =1, help = "Output name")
    ar = a.parse_args ( )
    
    if (ar.i and ar.o):
        imgName= ar.i[0]
        img = misc.imread(imgName + '.png', mode = 'L')
        imgNew = img

        if (ar.a):
           imgNew = rotation (imgNew, ar.a[0], ar.m[0])
           misc.imsave(imgName+'_Rotation.png',imgNew)
        if (ar.e):
           imgNew = scaleS(imgNew, ar.e[0], ar.m[0])
           misc.imsave(imgName+'_SingleScale.png',imgNew)
        if (ar.d):
           imgNew = scaleD(imgNew, ar.d[0], ar.d[1], ar.m[0])
           misc.imsave(imgName+'_DimensionScale.png',imgNew)            
        misc.imsave(ar.o[0]+'.png',imgNew)
    else:
        print "Insufficient arguments."
    

main ( )