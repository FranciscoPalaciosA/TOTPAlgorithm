import os
import cv2
import numpy as np
import random
from sklearn import ensemble
import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

USED_PAIR_OF_AXIS = 'x-z'

PAIRS_OF_AXIS = ['x-z']

movements = [
        'Circle',
        'Triangle',
        'Infinity',
        'Square',
        'S_Shape',
        'Diamond'
        ]

dataset = []
labels = []

for movement in movements:
    dir = f'./compress/shape/{movement}/{USED_PAIR_OF_AXIS}'
    for filename in os.listdir(dir):
        if filename != '.DS_Store':
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                img = cv2.imread(f)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dataset.append(gray)
                labels.append(movement)

# Get numpy dataset array
dataset = np.array(dataset)

# Get x & y
n_samples = len(dataset)
x = dataset.reshape((n_samples, -1))
y = labels
i = 0
for label in y:
    y[i] = movements.index(label)
    i += 1

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
