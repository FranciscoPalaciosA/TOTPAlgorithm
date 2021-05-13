import os
import cv2
import numpy as np
import random
from sklearn import ensemble
import joblib

from sklearn.model_selection import cross_val_score

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

def getClassifier(actual_classifier):
    if actual_classifier == 'RandomForestClassifier':
        return ensemble.RandomForestClassifier()
    elif actual_classifier == 'BaggingClassifier':
        return ensemble.BaggingClassifier()
    elif actual_classifier == 'AdaBoostClassifier':
        return ensemble.AdaBoostClassifier()
    elif actual_classifier == 'ExtraTreesClassifier':
        return ensemble.ExtraTreesClassifier()
    return ensemble.RandomForestClassifier()

methods_score = {
    "RandomForestClassifier": 0,
    "ExtraTreesClassifier": 0,
    "BaggingClassifier": 0,
}


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

# Get train and test indexes
sample_index = random.sample(range(len(x)), int((len(x)/5)*4))
valid_index = [i for i in range(len(x)) if i not in sample_index]

# Get samples to train
sample_images = [x[i] for i in sample_index]
sample_target = [y[i] for i in sample_index]

# Get samples to test
valid_images = [x[i] for i in valid_index]
valid_target = [y[i] for i in valid_index]

classifiers = [
        'RandomForestClassifier',
        'ExtraTreesClassifier',
        'BaggingClassifier'
        ]

runs = 5
for i in range(runs):
    print("Running - ", i)
    for actual_classifier in classifiers:
        print("   Doing ", actual_classifier)
        classifier = getClassifier(actual_classifier)
        classifier.fit(sample_images, sample_target)
        score = classifier.score(valid_images, valid_target)
        methods_score[actual_classifier] += score
        #joblib.dump(classifier, actual_classifier)

print(methods_score)
for method_name in methods_score:
    print(f"{method_name} - {(methods_score[method_name] * 100) / runs} %")
