# Image thresholding and labeling objects

In order to perform the operation to identify the contours of the objects it is necessary that the image go through a segmentation process. This will determine who is the subject in the image. Therefore, this script only work for simple images that the background of the test image is white, the command segmented = (img! = 255) is responsible for this segregation, separating the pixels of the image that have information other than white, that is, the objects. Subsequently, the function findBoundaries() is used with the segmented image as a parameter. The function used generates an array in which different regions are labeled. Thus, a pixel is considered an edge pixel if any of its neighbors have a different label.

For the next step of the implemented algorithm we have calculated some metrics such as centroid, perimeter and area of each identified object. The regionprops() function is able to get some measurements given a labeled image. Thus, the image was labeled when executing the line of code containing the command label(img). From the labeled image, we are able to calculate the metrics mentioned. Therefore, for each object labeled using object.centroid, object.area, object.perimeter and object.label is given the possibility of calculating the centroid and label of the image.

The last step of the algorithm requires the construction of an area histogram. We define three categories, small, medium and large with their respective intervals of (I) less than 1500; (II) between 1500 and 3000; (III) greater than 3000. An array then stores and counts the areas according to the divisions mentioned generating the histogram.

**Expected results:**

It is possible to observe below, respectively, the input image, the thresholding, the detection of the edges of the objects and finally the object labeling

![concept](objetos1.png)  ![concept](objetos1Segmented.png)  ![concept](objetos1Border.png)  ![concept](objetos1Label.png)
