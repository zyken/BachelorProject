import keras
import os
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

def getLabelsOfFolder(path):
    labels = []
    i = 0
    for subdir, dirs, files in os.walk(train_path):
        if i == 0:
            i += 1
            continue

        labels.append(subdir.split(os.path.sep)[-1])

    return labels



train_path = "../images/augmented_images/images_genus"
valid_path = "../images/val_augmented_images/images_genus"
test_path = "../images/test_augmented_images/images_genus"
labels = getLabelsOfFolder(train_path)

train_batches = ImageDataGenerator().flow_from_directory(train_path, target_size=(224, 224), classes=labels, batch_size=10)

valid_batches = ImageDataGenerator().flow_from_directory(valid_path, target_size=(224, 224), classes=labels, batch_size=4)


vgg16_model = keras.applications.vgg16.VGG16()

#vgg16_model.summary()

model = Sequential()
for layer in vgg16_model.layers:
    model.add(layer)

model.layers.pop()
for layer in model.layers:
    layer.trainable = False

model.add(Dense(44, activation="softmax"))

model.compile(Adam(lr=.0001), loss="categorical_crossentropy", metrics=["accuracy"])

#model.fit_generator(train_batches, steps_per_epoch=4, validation_data=valid_batches, epochs=5, verbose=2)
