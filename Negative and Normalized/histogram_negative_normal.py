#Basic image manipulation :
# Calculate statistical information
# Generate histogram
# Convert the input image to its negative
# Normalize image pixel values

from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

# open image file and stores it in a numpy array
imgName= raw_input()
img = misc.imread(imgName+'.png',mode ="L")

# image statistical information
imgWidth = img.shape[1]
imgHeight = img.shape[0]
imgMin = img.min()
imgMax = img.max()
mean = img.mean()

print "Largura: ",imgWidth
print "Altura: ",imgHeight
print "Intensidade minima: ",imgMin
print "Intensidade maxima: ",imgMax
print "Intensidade media: %.2f" % mean

#show image
plt.imshow(img, cmap='gray')
plt.imsave ('gray.png',img, cmap='gray')
plt.show()

# histogram
pixels = np.reshape(img, imgWidth*imgHeight)
plt.hist(pixels)
plt.show()

# image negative
negative = 255 - img
plt.imsave (imgName+'Negative.png',negative, cmap='gray')
plt.imshow(negative, cmap='gray')
plt.show ( )

# image normalized
normalized = (180-120)/float(imgMax-imgMin)*(img-imgMin)+ 120
misc.toimage(normalized, low = normalized.min(), high = normalized.max()).save(imgName+'Normalized.png')
misc.toimage(normalized, low = normalized.min(), high = normalized.max()).show ( )
















