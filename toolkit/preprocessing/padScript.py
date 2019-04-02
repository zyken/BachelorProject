from padImg import PadImageWhite
from imutils import paths
import cv2
import os

def padScript(dir):
    files = list(paths.list_images(dir))
    
    for f in files:
        im = cv2.imread(f)
        im = PadImageWhite(im, 1644, 1644)
        newf = f.split(os.path.sep)[-1]
        cv.imwrite(dir + '/../paddingOut' + newf)