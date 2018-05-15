from scipy import misc, stats
from PIL import Image
import numpy as np
from skimage import feature, io
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)

# hough image rotation
def Hough_Rotation (img, imgName):
    edges = feature.canny(img)
    h, theta, d = hough_line(edges)
    hac, angles, dists = hough_line_peaks(h, theta, d)

    deg = np.degrees(angles)
    angle = stats.mode(deg, axis = None).mode
    if (angle > 0):
        sumA = stats.mode(deg, axis = None).mode -90
    else:
        sumA = 90 + stats.mode(deg, axis = None).mode 

    print sumA

    matrix = misc.toimage(h)
    matrix.save(imgName+'_Hough.png')

    Nmpy2PIL = misc.toimage(img)
    imgR = Nmpy2PIL.rotate(sumA, resample = Image.BICUBIC)
    imgR.save(imgName+'_rotation_hough.png')

# gets histogram from image. Horizontal Projection is calculated based
# on number of black pixels per line
def Hist_Projection (img):
    edges = feature.canny(img)
    n = edges.shape[0]
    Hist = np.zeros (n)
    for i in range(n):
        Hist[i] = np.sum(edges[i]) 
    return Hist

# rotates image for angles (-90 to 90) and calculates projection
# finds angle that histogram is most relevant and rotate in angle
def HorizontalP_Rotation (img, histogram, imgName):
    angleMax = 0
    diff = 0
    edgesP = feature.canny(img)
    for i in range (91):
        imgRP = misc.imrotate(edgesP, i, interp = 'bicubic')
        hRP = Hist_Projection (imgRP)

        imgRN = misc.imrotate(edgesP, -i, interp = 'bicubic')
        hRN = Hist_Projection (imgRN)
        
        mseRP = ((histogram - hRP)**2).mean( )
        mseRN = ((histogram - hRN)**2).mean( )

        if (diff < mseRP):
            diff = mseRP
            angleMax = i
        elif(diff < mseRN):
            diff = mseRN
            angleMax = -i
    
    img_projection = misc.imrotate(img, angleMax, interp = 'bicubic')
    io.imsave(imgName+'_rotation_projection.png', img_projection)

# main function
def main ( ):
    imgName= raw_input()
    img = misc.imread(imgName+'.png',mode ="L")
    Hough_Rotation (img, imgName)

    histogram = Hist_Projection (img)
    HorizontalP_Rotation (img, histogram, imgName)

main ( )



























