import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.models import model_from_yaml
import matplotlib.pyplot as plt

img_height = 160
img_width = 140
images_to_test = [
        './x-z_movements/circle/-MWvRWuhSQ3-tQzw6OVg.png',
        './x-z_movements/square/-MX82CL5N4Fzbh_cb2wP.png',
        './x-z_movements/triangle/-MX3fRM_jp43-YfOv4Og.png',
        './x-z_movements/diamond/-MWvUl01UO-r5HLzcKuL.png',
        './x-z_movements/s_shape/-MX-Zq5WUBg35qszPY2l.png',
        './x-z_movements/infinity/-MX-YqBd4kmhtslvMUN6.png',
        './users_shapes/incorrect/S_Shape/x-z/-M_2UQ1JncDW1tsCic8_.png',
        './users_shapes/incorrect/Infinity/x-z/-M_3nggXJzBrejk1I2eB.png',
        './users_shapes/incorrect/Triangle/x-z/-M_44dPD5vIYZMpLP2Ub.png',
        './users_shapes/incorrect/Diamond/x-z/-M_43BIPkfwCu95xUJO9.png'
        ]

yaml_file = open('model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
loaded_model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

movements = [
        'Circle',
        'Diamond',
        'Infinity',
        'S_Shape',
        'Square',
        'Triangle',
        ]

predictions = []
images = []

for test_img in images_to_test:
    img = tf.keras.preprocessing.image.load_img(
            test_img,
            target_size=(img_height, img_width)
            )
    img_array = keras.preprocessing.image.img_to_array(img)
    images.append(img_array)
    img_array = tf.expand_dims(img_array, 0)

    prediction = loaded_model.predict(img_array)
    score = tf.nn.softmax(prediction[0])

    print(
        "This image most likely to be a {} with a {:.2f} percent confidence."
        .format(movements[np.argmax(score)], 100 * np.max(score))
    )
    predictions.append(movements[np.argmax(score)])

fig = plt.figure(figsize=(2, 5))
i = 0
for image in images:
    fig.add_subplot(2,5,i+1)
    plt.imshow(image)
    plt.xlabel(predictions[i])
    plt.title(images_to_test[i])
    i += 1

plt.show()

