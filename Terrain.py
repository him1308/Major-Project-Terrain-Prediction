import tensorflow as tf
from tensorflow import keras
from keras.layers import Flatten, Dense, Input, Dropout
from keras.models import Model
from keras.regularizers import l2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras.applications.xception import Xception

# Mount Google Drive (optional if your dataset is in Drive)
from google.colab import drive
drive.mount('/content/drive')

path = '/content/your_dataset_folder'  # <-- CHANGE THIS

# Data generator
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    zoom_range=[0.8, 1.2],
    horizontal_flip=True,
    vertical_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    path,
    subset='training',
    target_size=(229, 229),
    batch_size=32,
    class_mode='categorical',
    shuffle=True
)

val_data = datagen.flow_from_directory(
    path,
    subset='validation',
    target_size=(229, 229),
    batch_size=32,
    class_mode='categorical',
    shuffle=True
)

# Model building
input_tensor = Input(shape=(229, 229, 3))
base_model = Xception(include_top=False, input_tensor=input_tensor)
base_model.trainable = True  # Fine-tuning

x = Flatten()(base_model.output)
x = Dense(units=256, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(units=125, activation='relu')(x)
x = Dropout(0.3)(x)
output_tensor = Dense(units=5, activation='softmax')(x)

final_model = Model(inputs=input_tensor, outputs=output_tensor)

# Model checkpoint to save best model
checkpoint = ModelCheckpoint(
    '/content/best_model.keras',  # Save inside Colab environment
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)
callbacks = [checkpoint]

# Compile model
final_model.compile(
    loss='categorical_crossentropy',
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    metrics=['accuracy']
)

# Train model
history = final_model.fit(
    train_data,
    epochs=20,
    validation_data=val_data,
    callbacks=callbacks
)
