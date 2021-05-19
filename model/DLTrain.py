import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

USED_PAIR_OF_AXIS = 'x-z'
# movements = [
#         'Circle',
#         'Triangle',
#         'Infinity',
#         'Square',
#         'S_Shape',
#         'Diamond'
#         ]

img_height = 160
img_width = 140
batch_size = 64

train_db = tf.keras.preprocessing.image_dataset_from_directory(
        './x-z_movements',
        labels='inferred',
        label_mode='categorical',
        validation_split=0.2,
        subset='training',
        seed=4,
        image_size=(img_height, img_width),
        batch_size=batch_size
        )
test_db = tf.keras.preprocessing.image_dataset_from_directory(
        './x-z_movements',
        labels='inferred',
        label_mode='categorical',
        validation_split=0.2,
        subset='validation',
        seed=4,
        image_size=(img_height, img_width),
        batch_size=batch_size
        )

AUTOTUNE = tf.data.AUTOTUNE

train_db = train_db.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
test_db = test_db.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = 6

model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu', input_shape=(img_height, img_width, 3)),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='sigmoid'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              # loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              loss='mse',
              metrics=['accuracy'])
model.summary()

epochs=6
history = model.fit(
        train_db,
        validation_data=test_db,
        epochs=epochs,
        
        )

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.show()

model_yaml = model.to_yaml()
with open("model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
model.save_weights("model.h5")
print("Saved model to disk")

