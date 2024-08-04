import tensorflow as tf
from tensorflow.keras import layers, models 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np

# Load MNIST data from CSV
train_df = pd.read_csv('/Users/rohanwadhwa/Documents/emnist-digits-train.csv')  # Path to training CSV file
test_df = pd.read_csv('/Users/rohanwadhwa/Documents/emnist-digits-test.csv')    # Path to testing CSV file


X_train = train_df.iloc[:, 1:].values # gets the values of every row and column except the first one
Y_train = train_df.iloc[:, 0].values # gets the values of every row from the first column

X_test = test_df.iloc[:, 1:].values # gets the values of every row and column except the first one
Y_test = test_df.iloc[:, 0].values# gets the values of every row from the first column

# Normalize the data
X_train, X_test = X_train / 255.0, X_test / 255.0

# Reshape the data to fit the model's expected input shape
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)


train_datagen = ImageDataGenerator(
    
    rotation_range=10,      # Randomly rotate images in the range (degrees, 0 to 180)
    width_shift_range=0.1,  # Randomly translate images horizontally (fraction of total width)
    height_shift_range=0.1, # Randomly translate images vertically (fraction of total height)
    shear_range=0.1,        # Randomly shear transformations
    zoom_range=0.1,         # Randomly zoom images
    horizontal_flip=False,  # Randomly flip images horizontally (not relevant for digit recognition)
    fill_mode='nearest'     # Fill in new pixels with nearest values
)
    
    
# No augmentation for validation data, only rescale
validation_datagen = ImageDataGenerator()

# Create generators for training and validation
train_generator = train_datagen.flow(X_train, Y_train, batch_size=32)
test_generator = train_datagen.flow(X_test, Y_test, batch_size=32)

model = models.Sequential([
    layers.Conv2D(80, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    # Applies 80 filters (kernels) of size 3x3 to the input, 
    # producing 80 feature maps. The ReLU activation function adds non-linearity.
    # The input shape is specified as (28, 28, 1) for grayscale images of size 28x28.

    layers.MaxPooling2D((2, 2)),
    # Performs max pooling with a 2x2 window, reducing the height and width of the feature maps by half.
    # This operation helps to reduce the spatial dimensions, allowing the model to focus on the most salient features.

    layers.Conv2D(80, (3, 3), activation='relu'),
    # Adds another convolutional layer with 80 filters of size 3x3 and ReLU activation,
    # further extracting features from the input data.

    layers.MaxPooling2D((2, 2)),
    # Another max pooling layer with a 2x2 window to further reduce the spatial dimensions.

    layers.Flatten(),
    # Flattens the 3D output from the previous layer into a 1D vector,
    # preparing it for input into the fully connected (dense) layers.

    layers.Dense(100, activation='relu'),
    # A fully connected (dense) layer with 100 units and ReLU activation,
    # learning non-linear combinations of the features extracted by the convolutional layers.

    layers.Dense(50, activation='relu'),
    # A fully connected (dense) layer with 50 units and ReLU activation,
    # learning non-linear combinations of the features extracted by the convolutional layers.
    
    layers.Dense(10, activation='softmax')
    # The output layer with 10 units (one for each digit class, 0-9),
    # using the softmax activation function to produce a probability distribution over the 10 classes.
   
])

#Compiles the model using an adam optimization algorithm to adjust the weights and loss function to
#calculate the loss based on predicted label and actual label
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        
#Fitting the model with the training dataset and the testing dataset for evaluation of the model's performance
model.fit(train_generator, epochs=7, validation_data=(test_generator))

#Evaluating the model with test loss being the input testing data and the accuracy being the output testing data(actual labels)
test_loss, test_acc = model.evaluate(test_generator)
print(f"Test accuracy: {test_acc}")

#Saves the model
model.save('mnist_model.keras')






 



