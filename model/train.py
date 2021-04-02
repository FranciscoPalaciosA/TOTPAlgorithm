# import matplotlib.pyplot as plt
# import pylab as pl
# import cv2
# import scipy

# pl.gray()
# Save image in set directory
# Read RGB image
# image = cv2.imread('./shape/Circle/w-x/-MWvOk5Ge6eV0ayub45k.png')
# pl.matshow(img)
# pl.show()
# print(img)
# scipy.misc.imread()
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# print(gray.shape)
# cv2.imwrite('./shape/Circle/w-x/compressed/-MWvOk5Ge6eV0ayub45k.png', gray, [cv2.IMWRITE_PNG_COMPRESSION, 9])
# image2 = cv2.imread('./shape/Circle/w-x/compressed/-MWvOk5Ge6eV0ayub45k.png')
# print(image2.shape)
# print(gray)

import os
import cv2
import numpy as np
import random
from sklearn import ensemble

USED_PAIR_OF_AXIS = 'x-z'
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
    dir = f'./shape/{movement}/{USED_PAIR_OF_AXIS}'
    for filename in os.listdir(dir):
        if filename != '.DS_Store':
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                img = cv2.imread(f)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                dataset.append(gray)
                labels.append(movement)
dataset = np.array(dataset)

# for index, (image, label) in enumerate(dataset[:100]):
#     print(image.shape, label)

n_samples = len(dataset)
x = dataset.reshape((n_samples, -1))
y = labels

sample_index = random.sample(range(len(x)), int((len(x)/5)*4))
valid_index = [i for i in range(len(x)) if i not in sample_index]

sample_images = [x[i] for i in sample_index]
valid_images = [x[i] for i in valid_index]

sample_target = [y[i] for i in sample_index]
valid_target = [y[i] for i in valid_index]

classifier = ensemble.RandomForestClassifier()

classifier.fit(sample_images, sample_target)

score = classifier.score(valid_images, valid_target)
print(f'SCORE - \t{str(score)}')

tests = ['-MXI5l9EVJeYUXvp8eDz', '-MXI9Ew5TPIRcCukj0Qc', '-MXIAuDDav93CUv-U-gr']
for test in tests:
    test_shape = cv2.imread(f'./tests/shape/Infinity/{USED_PAIR_OF_AXIS}/{test}.png')
    grayed_test = cv2.cvtColor(test_shape, cv2.COLOR_BGR2GRAY)
    print(classifier.predict(grayed_test.reshape(1,-1)))
    print(classifier.predict_proba(grayed_test.reshape(1,-1)))
    print(classifier.classes_)