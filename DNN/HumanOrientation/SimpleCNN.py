from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten,Dense
from keras import backend as k

from model import DirectionModel as DM

#Image dimentions
img_width, img_height = 150,150

train_directory = "data/train"
validation_directory = "data/validation"
test_directory= "test"

nb_train_samples = 246*4
nb_validatioin_sample = 41*4
epochs = 5
batch_size = 15

input_shape = (img_width, img_height, 3)
model = DM.make_model(input_shape)


model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

#make more data
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=False)

test_datagen = ImageDataGenerator(rescale=1. /255)

train_generator = train_datagen.flow_from_directory(train_directory,
                                                    target_size=(img_width, img_height),
                                                    batch_size=batch_size,
                                                    class_mode='categorical')
print("Lables")
label_map = (train_generator.class_indices)
print(label_map)

validation_generator = test_datagen.flow_from_directory(validation_directory,
                                                        target_size=(img_width, img_height),
                                                        batch_size=batch_size,
                                                        class_mode='categorical')


model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples//batch_size,
    epochs = epochs,
    validation_data = validation_generator,
    validation_steps= nb_validatioin_sample // batch_size
)

#Save the model as well as the weights
model.save('first_model.h5')
model.save_weights('first_weights.h5')

print("Lables")
print(label_map)
