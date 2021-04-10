import os
import cv2
import numpy as np
import random
from sklearn import ensemble
import joblib

USED_PAIR_OF_AXIS = 'x-z'
movements = [
        'Circle',
        ]
dataset = []
labels = []

def get_avg(arr):
    s = 0
    for i in arr:
        s = s + i
    return 255 -  s / len(arr)

def compress_matrix(matrix):
    h, w = matrix.shape
    print("H, w = ", h, w)
    new_h = int(h / 4)
    new_w = int(w / 4)
    jump = 4

    compressed_matrix = np.zeros((new_h, new_w))
    print("compressed shape = ", compressed_matrix.shape)
    for i in range(new_h):
        for j in range(new_w):
            nums_to_avg = []
            for k in range(4):
                for l in range(4):
                    nums_to_avg.append(matrix[i * jump + k][j * jump + l])
            compressed_matrix[i][j] = get_avg(nums_to_avg)
    
    print(compressed_matrix.shape)
    print("Compressed = ", compressed_matrix)
    cv2.imwrite('./compress/shape/compressed.jpg', compressed_matrix)
    cv2.imshow("image", compressed_matrix)


for movement in movements:
    dir = f'./compress/shape/{movement}/{USED_PAIR_OF_AXIS}'
    for filename in os.listdir(dir):
        if filename != '.DS_Store':
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                img = cv2.imread(f)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                compressed = compress_matrix(gray)
                dataset.append(gray)
                labels.append(movement)

# Get numpy dataset array
#  dataset = np.array(dataset)

# Get x & y
#  n_samples = len(dataset)
#  x = dataset.reshape((n_samples, -1))
#  y = labels

# Get train and test indexes
#  sample_index = random.sample(range(len(x)), int((len(x)/5)*4))
#  valid_index = [i for i in range(len(x)) if i not in sample_index]

# Get samples to train
#  sample_images = [x[i] for i in sample_index]
#  sample_target = [y[i] for i in sample_index]

# Get samples to test
#  valid_images = [x[i] for i in valid_index]
#  valid_target = [y[i] for i in valid_index]



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

classifiers = [
        'RandomForestClassifier',
        # 'BaggingClassifier',
        # 'AdaBoostClassifier',
        # 'ExtraTreesClassifier'
        ]

# for actual_classifier in classifiers:
#     classifier = getClassifier(actual_classifier)
#     classifier.fit(sample_images, sample_target)
#     score = classifier.score(valid_images, valid_target)
#     print(f'{actual_classifier} SCORE - \t{str(score)}')
#     joblib.dump(classifier, actual_classifier)

