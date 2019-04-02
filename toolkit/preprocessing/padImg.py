import numpy as np
import cv2 as cv 

def PadImage(im, wmax, hmax, paddingcolor):
        height, width, dim = im.shape

        if width > wmax or height > hmax:
            raise Exception('picture dimensions are larger than scaling dimansions')

        top = (hmax - height) // 2
        bot = hmax - top - height
        left = (wmax - width) // 2
        right = wmax - width - left
        im = cv.copyMakeBorder(im, top, bot, left, right, cv.BORDER_CONSTANT, value=paddingcolor)
        if im.shape[0] != hmax or im.shape[1] != wmax:
            raise Exception("Something went wrong with dimensions..")
        return im

def PadImageWhite(im, wmax, hmax):
        height, width, dim = im.shape

        if width > wmax or height > hmax:
            raise Exception('picture dimensions are larger than scaling dimansions')

        top = (hmax - height) // 2
        bot = hmax - top - height
        left = (wmax - width) // 2
        right = wmax - width - left
        im = cv.copyMakeBorder(im, top, bot, left, right, cv.BORDER_CONSTANT, value=[255., 255., 255.])
        if im.shape[0] != hmax or im.shape[1] != wmax:
            raise Exception("Something went wrong with dimensions..")
        return im