# Data comes from http://benchmark.ini.rub.de/?section=gtsdb&subsection=dataset
# Processed files can be found here https://d17h27t6h515a5.cloudfront.net/topher/2017/February/5898cd6f_traffic-signs-data/traffic-signs-data.zip
import warnings
warnings.filterwarnings("ignore")

# Need to read in data files
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix

# Data set locations and paths
trainingPath = "TrainingData/train.p"
testingPath = "TrainingData/test.p"
validationPath = "TrainingData/valid.p"

# Get the data from the data sets using pickle to read them in
with open(trainingPath, mode="rb") as training_data:
    train = pickle.load(training_data)

with open(testingPath, mode="rb") as testing_data:
    test = pickle.load(testing_data)

with open(validationPath, mode="rb") as validation_data:
    valid = pickle.load(validation_data)

# Create the features and labels for the data and link them
x_train, y_train = train['features'], train['labels']
x_test, y_test = test['features'], test['labels']
x_validation, y_validation = valid['features'], valid['labels']

# Check to see if it imported right as well as the shape for each set
print("X Sahpe", x_train.shape)
print("Y shape", y_train.shape)

# Data prearation
# Shuffle data only the training data
x_train, y_train = shuffle(x_train, y_train)

# Turn to gray images
x_train_gray = np.sum(x_train/3, axis=3, keepdims=True)
x_test_gray = np.sum(x_test/3, axis=3, keepdims=True)
x_validation_gray = np.sum(x_validation/3, axis=3, keepdims=True)

# Normalize the images
x_train_gray_norm = (x_train_gray - 128)/128
x_test_gray_norm = (x_test_gray - 128)/128
x_validation_gray_norm = (x_validation_gray - 128)/128

# Check the shape of the gray
print("X Gray Shape", x_train.shape)

# Check to see if graying worked
i = 610
plt.imshow(x_train_gray[i].squeeze(), cmap='gray')
plt.figure()
plt.imshow(x_train[i])


# Model Training

# Define Image Shape
image_shape = x_train_gray[i].shape

# Create a sequential model
cnn_model = Sequential()
cnn_model.add(Conv2D(32,3, 3, input_shape = image_shape, activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Flatten())
cnn_model.add(Dense(output_dim = 32, activation = 'relu'))
cnn_model.add(Dense(output_dim = 43, activation = 'sigmoid'))

cnn_model.compile(loss ='sparse_categorical_crossentropy', optimizer=Adam(lr=0.001),metrics =['accuracy'])

history = cnn_model.fit(x_train_gray_norm,
                        y_train,
                        batch_size=500,
                        nb_epoch=50,
                        verbose=1,
                        validation_data = (x_validation_gray_norm,y_validation))


score = cnn_model.evaluate(x_test_gray_norm, y_test,verbose=0)
print('Test Accuracy : {:.4f}'.format(score[1]))


accuracy = history.history['acc']
val_accuracy = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(accuracy))
plt.plot(epochs, accuracy, 'bo', label='Training Accuracy')
plt.plot(epochs, val_accuracy, 'b', label='Validation Accuracy')
plt.title('Training and Validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'bo', label='Training Loss')
plt.plot(epochs, val_loss, 'b', label='Validation Loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()


#get the predictions for the test data
predicted_classes = cnn_model.predict_classes(x_test_gray_norm)
#get the indices to be plotted
y_true = y_test

cm = confusion_matrix(y_true, predicted_classes)


for i in range(0,12):
    plt.subplot(4,3,i+1)
    plt.imshow(x_test_gray_norm[i+10].squeeze(), cmap='gray', interpolation='none')
    plt.title("Predicted {}, Class {}".format(predicted_classes[i+10], y_true[i+10]))
    plt.tight_layout()
