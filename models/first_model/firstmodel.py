import sys
sys.path.append("..")
from keras.applications import ResNet50
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras_preprocessing.image import ImageDataGenerator
from toolkit import getLabelsFromDir
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# setup
batch_size = 3
steps_per_epoch = int(12525/batch_size) + 1
validation_steps = int(3454/batch_size) + 1

### Model building ####

base_model = ResNet50(
            include_top=False,
            input_shape=(224, 224, 3),
            weights='imagenet')

# we only train on the output layer (the fully connected layers 'predictions' below)
base_model.trainable = False

#add a new dense layer to the end of the network inplace of the old layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)

# add the outplut layer
predictions = Dense(44, activation='softmax')(x)

# create new model composed of pre-trained network and new final layers
model = Model(input=base_model.input, output=predictions)
model.summary()

# compile model
model.compile(loss='categorical_crossentropy',
            optimizer='sgd',
            metrics=['accuracy'])

train_dir = "../../images/images_genus/train/"
val_dir = "../../images/images_genus/val/"

assert(getLabelsFromDir(train_dir) == getLabelsFromDir(val_dir))
labels = getLabelsFromDir(train_dir)

train_datagen = ImageDataGenerator(rescale=1./255.)
val_datagen = ImageDataGenerator(rescale=1./255.)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    classes=labels,
                                                    class_mode="categorical",
                                                    batch_size=batch_size,
                                                    color_mode='rgb',
                                                    target_size=(224, 224) )
val_generator = train_datagen.flow_from_directory(val_dir,
                                                    classes=labels,
                                                    class_mode="categorical",
                                                    batch_size=batch_size,
                                                    color_mode='rgb',
                                                    target_size=(224, 224) )

#Train
model.fit_generator(train_generator,
                    steps_per_epoch=steps_per_epoch,
                    epochs=5,
                    validation_data=val_generator,
                    validation_steps=validation_steps)

#save
model.save("resnet50_first.h5")