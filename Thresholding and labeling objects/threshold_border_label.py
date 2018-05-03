# Script to perform a simple segmentation by thresholding
# Detect the edges of segmented objects
# Define the centroid of the object and write a label
# Show histogram of the size of the identified objects

from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
from skimage import segmentation
from skimage.measure import label, regionprops
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import matplotlib.pyplot as plt; plt.rcdefaults()
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

#print "Dimensions: ",imgChannel
print "Largura: ",imgWidth
print "Altura: ",imgHeight
print "Intensidade minima: ",imgMin
print "Intensidade maxima: ",imgMax
print "Intensidade media: %.2f" % mean

#Apply segmentation
segmented = (img != 255)
misc.toimage(segmented).show ( )
misc.toimage(segmented).save(imgName+'Segmented.png')

#show image
plt.imshow(img, cmap='gray')
plt.imsave (imgName+'Gray.png',img, cmap='gray')
plt.show()

#Extract borders
border = segmentation.find_boundaries(segmented)
misc.toimage(border).show ( )
misc.toimage(border).save(imgName+'Border.png')

#Apply Label
label_img = label(segmented)
props = regionprops(label_img)
arrayArea = np.zeros (3)

# Get object properties
for i in props:
    center = i.centroid
    ar = i.area
    pmtr = i.perimeter
    lbl = i.label
    print "Region: ",lbl ,"\tPerimeter: ", pmtr, "\tArea: ", ar ,"\tCenter: ", center
    #Array for building the histogram
    if (ar < 1500):
        arrayArea[0] = arrayArea[0] + 1
    elif (ar >= 1500 and ar < 3000):
        arrayArea[1] = arrayArea[1] + 1
    else: 
        arrayArea[2] = arrayArea[2] + 1


pil = misc.toimage (border)
draw = ImageDraw.Draw(pil)
font = ImageFont.load_default()
# Label the border image
for i in props:
    draw.text((i.centroid[1],i.centroid[0]),str(i.label),(255,255,255),font=font)
pil.show ( )
pil.save(imgName+'Label.png')


#Generate histogram
objects = ('Small', 'Medium', 'Large')
y_pos = np.arange(len(arrayArea))
performance = [arrayArea[0],arrayArea[1],arrayArea[2]]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Number of Objects')
plt.title('Area Size')
 
plt.show()




