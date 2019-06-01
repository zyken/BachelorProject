import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from os import listdir

#counts pixel from one end of a ruler to the other and returns 
#the pixels divided by the dist specified by the input
def getPSize(binImage, rulerDist, imgName=""):
    dists = []
    r, c = binImage.shape
    for row in range(r):
        p1 = 0
        p2 = 0
        i = 0
        try:
            #find first 2 border pixels
            while p1 == 0:
                if binImage[row, i] != 0 and binImage[row, i + 1] != 0:
                    p1 = i
                    i += 1
                i += 1
                if i == c:
                    raise("could not find solution to image " + imgName)
            
            #find end of first ruler line
            while binImage[row, i] != 0 and binImage[row, i + 1] != 0:
                i += 1
                if i == c:
                    raise("could not find solution to image " + imgName)

            #find start of second ruler line
            while p2 == 0:
                if binImage[row, i] != 0 and binImage[row, i + 1] != 0:
                    p2 = i
                    break
                i += 1
                if i == c:
                    raise("could not find solution to image " + imgName)
        except:
            return 0.0
             
        dists.append(p2 - p1)
    return np.mean(dists) / float(rulerDist)


if __name__ == "__main__":
    dirPath = '/media/david/MyBackup/2019_03_07/'
    imgFiles = listdir(dirPath)
    distInCm = 3.0
    outp = open("out.csv", "w")
    pixelSizes = [] #assuming quadratic pixels

    for f in imgFiles:
        img = misc.imread(dirPath + '/' + f, mode="L")
        dims = img.shape
        scaleInfo = img[dims[0]-40:dims[0], 2500:4000]
        scaleInfo = scaleInfo > 86
        # pixelSizes.append(getPSize(scaleInfo, distInCm, f))
        outp.write(str(getPSize(scaleInfo, distInCm, f)) + ",\n")
        # plt.imshow(scaleInfo, cmap='gray')
        # plt.show()
    print("max: ", np.max(pixelSizes), "min: ", np.min(pixelSizes))

