import os
import sys
import cv2
import numpy as np
import random
from sklearn import ensemble
import joblib

from sklearn.model_selection import cross_val_score

USED_PAIR_OF_AXIS = 'x-z'
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


def get_users_movements(correct):
    dir_str = './users_shapes/incorrect'
    if correct:
        dir_str = './users_shapes/correct'
    movements = sorted(os.listdir(dir_str))

    for movement in movements:
        if movement != '.DS_Store':
            dir = f'./users_shapes/correct/{movement}/{USED_PAIR_OF_AXIS}'
            for filename in os.listdir(dir):
                if filename != '.DS_Store':
                    f = os.path.join(dir, filename)
                    if os.path.isfile(f):
                        img = cv2.imread(f)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        dataset.append(gray)
                        labels.append(movement)

def get_both_users_movements():
    get_users_movements(True)
    get_users_movements(False)

def get_my_movements():
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

def reset_arrays():
    dataset = []
    labels = []

def train():
    # Get numpy dataset array
    m_dataser = np.array(dataset)

    # Get x & y
    n_samples = len(m_dataser)
    print("Samples length = ", n_samples)
    x = m_dataser.reshape((n_samples, -1))
    y = labels

    classifiers = [
        'RandomForestClassifier',
        'ExtraTreesClassifier',
        #'BaggingClassifier'
        ]

    runs = 20
    previous_score = 0
    for i in range(runs):
        # Get train and test indexes
        sample_index = random.sample(range(len(x)), int((len(x)/5)*4))
        valid_index = [i for i in range(len(x)) if i not in sample_index]

        # Get samples to train
        sample_images = [x[i] for i in sample_index]
        sample_target = [y[i] for i in sample_index]

        # Get samples to test
        valid_images = [x[i] for i in valid_index]
        valid_target = [y[i] for i in valid_index]
        print(" - Running - ", i)
        for actual_classifier in classifiers:
            #print("   Doing ", actual_classifier)
            classifier = getClassifier(actual_classifier)
            classifier.fit(sample_images, sample_target)
            score = classifier.score(valid_images, valid_target)
            print("    -  ", actual_classifier, score)
            methods_score[actual_classifier] += score
            if score > previous_score:
                print('   -  highest score = ', score)
                previous_score = score
                joblib.dump(classifier, actual_classifier)

    for method_name in methods_score:
        print(f"  --  {method_name} - {(methods_score[method_name] * 100) / runs} %")
    
def train_all():
    get_my_movements()
    get_both_users_movements()
    train()
    reset_arrays()

def train_both_correct():
    get_my_movements()
    get_users_movements(True)
    train()
    reset_arrays()

def train_users_all():
    get_both_users_movements()
    train()
    reset_arrays()

def train_users_correct():
    get_users_movements(True)
    train()
    
    reset_arrays()

def run():
    try:
        if sys.argv[1] == "all":
            print("Training with All (users and mine) - ")
            train_all()
        if sys.argv[1] == "both_correct":
            print("Training with both correct (users correct and mine) - ")
            train_both_correct()            
        if sys.argv[1] == "users_all":
            print("Training with users all (users all) - ")
            train_users_all()
        if sys.argv[1] == "users_correct":
            print("Training with users correct (users correct) - ")

    except IndexError:
      print('\n--- usage: script [all, both_correct, users_all, users_correct]\n')

run()