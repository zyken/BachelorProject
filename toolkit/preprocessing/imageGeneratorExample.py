from keras_preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
from padImg import PadImageWhite

def prepFunc(img):
    return PadImageWhite(img, 1000, 1000)

datagen = ImageDataGenerator(preprocessing_function=None, rescale=1./255, horizontal_flip=True, rotation_range=90)
labels = ['bille1', 'bille2']
data_path = "/home/herri/Documents/bachelor/TEST"

x = datagen.flow_from_directory(data_path, target_size=(256, 256), \
                    color_mode='rgb', class_mode='sparse',\
                    batch_size=3,save_prefix='', save_format='jpg', shuffle=True)

while 1:
    b = x.next()
    for i in range(3):
        img = b[0][i]
        print(b[1])
        plt.figure()
        # plt.title(labels[b[1]])
        plt.imshow(img)
        plt.colorbar()
        plt.grid(False)
        plt.show()
    input()
