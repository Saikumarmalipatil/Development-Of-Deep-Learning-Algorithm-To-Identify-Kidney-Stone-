import os 
from tensorflow.compat.v1 import ConfigProto 
from tensorflow.compat.v1 import InteractiveSession 
from tensorflow.keras.layers import Flatten, Dense, GlobalAveragePooling2D, Dropout 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.applications.inception_v3 import InceptionV3 
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
import matplotlib.pyplot as plt 

# Configure GPU memory usage 

config = ConfigProto() 
config.gpu_options.per_process_gpu_memory_fraction = 0.5 
config.gpu_options.allow_growth = True 
session = InteractiveSession(config=config) 

# Define image size 

IMAGE_SIZE = [224, 224] 

# Define paths to training and validation data 

train_path = "C:/Users/Saiku/OneDrive/Documents/Dataset/Train" 
valid_path = "C:/Users/Saiku/OneDrive/Documents/Dataset/Test"

# Define model saving path 

save_dir = "C:/Users/Saiku/Downloads/models.h5"

# Load InceptionV3 model pretrained on ImageNet without the top layer 
inception = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', 
include_top=False) 

# Freeze the first few layers

for layer in inception.layers[:100]: 
layer.trainable = False 

# Create a Sequential model 
model = Sequential() 

# Add InceptionV3 base model 
model.add(inception) 

# Add GlobalAveragePooling2D layer 
model.add(GlobalAveragePooling2D()) 

# Add dropout layer 
model.add(Dropout(0.5))  # Adjust dropout rate as needed 

# Add a dense layer with sigmoid activation for binary classification 
model.add(Dense(1, activation='sigmoid')) 

# Compile the model 
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 

# Data Augmentation 
train_datagen = ImageDataGenerator( 
rescale=1./255, 
shear_range=0.2, 
zoom_range=0.2, 
horizontal_flip=True 
) 
test_datagen = ImageDataGenerator(rescale=1./255) 

# Load the training and validation datasets 
training_set = train_datagen.flow_from_directory(train_path, target_size=(224, 224), 
batch_size=32, class_mode='binary') 
test_set = test_datagen.flow_from_directory(valid_path, target_size=(224, 224), 
batch_size=32, class_mode='binary') 

# Train the model with verbose set to 1 to track loss 
history = model.fit(training_set, validation_data=test_set, epochs=20, 
steps_per_epoch=len(training_set), validation_steps=1, verbose=1) 

# Plot accuracy curve 
plt.plot(history.history['accuracy'], label='Training Accuracy') 
plt.plot(history.history['val_accuracy'], label='Validation Accuracy') 
plt.title('Training and Validation Accuracy') 
plt.xlabel('Epochs') 
plt.ylabel('Accuracy') 
plt.legend() 
plt.show() 

# Plot loss curve (separate call to plt.plot) 
plt.plot(history.history['loss'], label='Training Loss') 
plt.plot(history.history['val_loss'], label='Validation Loss') 
plt.title('Training and Validation Loss') 
plt.xlabel('Epochs') 
plt.ylabel('Loss') 
plt.legend() 
plt.show() 

# Evaluate the model on the test set 
test_loss, test_accuracy = model.evaluate(test_set) 
print("Test Loss:", test_loss) 
print("Test Accuracy:", test_accuracy) 

# Create directory only if it doesn't exist (avoids errors) 
os.makedirs(save_dir, exist_ok=True) 

# Save the model 
save_path = os.path.join(save_dir, "model_inceptionv3t1.h5") 
model.save(save_path) 
print("Model saved at:", save_path)