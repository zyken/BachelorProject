import numpy as np
import cv2
import os
from imutils import paths

def otsu_seg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0) # Remove noise

    # find threshold using otsu's algorithm
    ret,thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # light spots in beetle will be remove as background unless we blur the thresh image a little
    thresh2 = cv2.GaussianBlur(thresh, (5,5), 0)
    thresh2[thresh2 > 0] = 255

    mask = np.array(thresh2, copy=True) # get dimension for mask
    mask[mask > 0] = 1
    mask = np.logical_not(mask)

    img_seg = img.copy() # create copy instead of alternating original image
    img_seg[mask] = 0

    return img_seg

def otsu_and_edge_seg(img):
    def edgedetect (channel): # RGB channel
        sobelX = cv2.Sobel(channel, cv2.CV_16S, 1, 0)
        sobelY = cv2.Sobel(channel, cv2.CV_16S, 0, 1)
        sobel = np.hypot(sobelX, sobelY)

        sobel[sobel > 255] = 255

        return sobel

    def findSignifContours(img, edgeImg):
        major = cv2.__version__.split('.')[0]
        if major == 3:
            _, contours, hierarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # ------- HEURESTIC ---------
        # From among contours, find the contours with surface area > 15% of image,
        # and surface area < 90% of image
        significant = []
        tooSmall = edgeImg.size * 15/100
        tooBig = edgeImg.size * 90/100

        # loop over contours. Would be more optimal to loop over level1,
        # i.e. top hierarchy, but then there is a need to fix if level1 does not
        # contain beetle, i.e. beetle-contour is child of bigger contour.
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > tooSmall and tooBig > area:
                significant.append([contour, area])

        return [x[0] for x in significant]

    img_otsu = otsu_seg(img)
    edge_img = np.max(
        np.array([edgedetect(img_otsu[:,:,0]),
        edgedetect(img_otsu[:,:,1]),
        edgedetect(img_otsu[:,:,2])]),
        axis=0)

    edge_img_8u = np.asarray(edge_img, np.uint8) # cv2.findContours in findSignifContours need edgeImg of type uint8
    significant = findSignifContours(img_otsu, edge_img_8u)

    mask = edge_img.copy()
    mask[mask > 0] = 0
    cv2.fillPoly(mask, significant, 1)
    mask = np.logical_not(mask)
    img_otsu[mask] = 0

    return img_otsu

class DatasetLoader:
    def __init__(self, preprocessers=None):
        # store img preprocessor
        self.preprocessors = preprocessers

        # if self.preprocessors == None:
        #     self.preprocessors = []

    def load(self, imagePaths, classLevel=-2, verbose=-1):
        # classlevel -2 = path_to_img/{class}/img
        # classlevel -3 = path_to_img/{class}/folder/img
        data = []
        labels = []

        for (i, imagePath) in enumerate(imagePaths):

            image = cv2.imread(imagePath)
            label = imagePath.split(os.path.sep)[classLevel]

            if self.preprocessors is not None:
                for p in self.preprocessors:
                    image = p(image)

            data.append(image)
            labels.append(label)

            if verbose > 0 and i > 0 and (i+1)%verbose == 0:
                print("[INFO] preprocessed {}/{}".format(i+1,len(imagePaths)))

        return (np.array(data), np.array(labels))

    def dataGenerator(self, rootdir, batchsize, classLevel=-2):
        imgpaths = list(paths.list_images(rootdir))
        length = len(imgpaths)

        #this line is just to make the generator infinite, keras needs that
        while True:

            batch_start = 0
            batch_end = batchsize

            while batch_start < length:
                limit = min(batch_end, length)
                X,Y = self.load(imgpaths[batch_start:limit])

                yield (X,Y) #a tuple with two numpy arrays with batch_size samples

                batch_start += batchsize
                batch_end += batchsize
