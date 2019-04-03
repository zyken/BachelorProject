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

#add a new dense layer to the end of the network inplace of the old layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)

# add the outplut layer
predictions = Dense(44, activation='softmax')(x)

# create new model composed of pre-trained network and new final layers
model = Model(input=base_model.input, output=predictions)

# we only train on the fully connected layers (the last two layers)
for layer in model.layers[:-2]:
    layer.trainable = False

model.summary()

# compile model
model.compile(loss='categorical_crossentropy',
            optimizer='sgd',
            metrics=['accuracy'])

train_dir = "../images/augmented_images/images_genus/train/"
val_dir = "../images/augmented_images/images_genus/val/"

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
model.save("restnet50.h5")

#Confution Matrix and Classification Report
Y_pred = model.predict_generator(val_generator, steps=validation_steps)
y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
print(confusion_matrix(val_generator.classes, y_pred))
print('Classification Report')
target_names = ['Cats', 'Dogs', 'Horse']
print(classification_report(val_generator.classes, y_pred, target_names=target_names))
