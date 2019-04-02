from keras_preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np

datagen = ImageDataGenerator(rescale=1./255)
labels = ['bille1', 'bille2']
data_path = "/home/herri/Documents/bachelor/TEST"

x = datagen.flow_from_directory(data_path, target_size=(500, 500), \
                    color_mode='rgb', class_mode='categorical',\
                    batch_size=3,save_prefix='', save_format='jpg')

while 1:
    b = x.next()
    for i in range(3):
        img = b[0][i]
        plt.figure()
        plt.title(labels[np.argmax(b[1][i])])
        plt.imshow(img)
        plt.colorbar()
        plt.grid(False)
        plt.show()
    input()
