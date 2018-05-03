# Negative and Normalized

Given an input image, the script calculates some basic statistics. Among the measures mentioned are the image width and height dimensions, maximum, minimum and average intensity. The histogram is calculated from a vector that contains the values of each pixel in the image. Therefore, the counting of each gray level present in the input vector is performed, subsequently generating a histogram illustrated by a graph containing frequency of each.

The third operation gets the negative from the image. Since in this operation the gray level 0 will be converted to 255 and so on, the calculation used is shown in the formula below, where intMax equals the maximum intensity of an 8-bit (255 grayscale) image, intM in the minimum intensity ( 0 grayscale) and img is the pixel of the original image that we are currently changing.

>Negative = intMax − (img + intMin)

The last procedure is to convert the range of intensities of the input image. Considering imgMax and imgMin the maximum and minimum intensity of the image respectively and img the pixel of the original image being altered. In addition, assuming MaxN as the new maximum intensity value and MinN as the new minimum intensity, the calculation used was:

>Norm =[(MaxN − MinN)/(imgMax − imgMin)]∗(img − imgMin) + MinN

