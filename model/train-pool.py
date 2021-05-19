import os
import sys
import cv2
import numpy as np
from sklearn import ensemble
import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

USED_PAIR_OF_AXIS = 'x-z'
movements = [
        'Circle',
        'Triangle',
        'Infinity',
        'Square',
        'S_Shape',
        'Diamond'
        ]
classifiers = [
        'RandomForestClassifier',
        'ExtraTreesClassifier',
        # 'MLPClassifier'
        ]
methods_score = {
    "RandomForestClassifier": 0,
    "ExtraTreesClassifier": 0,
}
dataset = []
labels = []

def getClassifier(actual_classifier):
    if actual_classifier == 'RandomForestClassifier':
        return ensemble.RandomForestClassifier()
    elif actual_classifier == 'BaggingClassifier':
        return ensemble.BaggingClassifier()
    elif actual_classifier == 'AdaBoostClassifier':
        return ensemble.AdaBoostClassifier()
    elif actual_classifier == 'ExtraTreesClassifier':
        return ensemble.ExtraTreesClassifier()
    elif actual_classifier == 'MLPClassifier':
        return MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
    return ensemble.RandomForestClassifier()

def get_users_movements(correct):
    correctIncorrect = 'incorrect'
    if correct:
        correctIncorrect = 'correct'
    dir_str = f'./users_shapes/{correctIncorrect}'
    funMovements = sorted(os.listdir(dir_str))
    for movement in funMovements:
        if movement != '.DS_Store' and movement in movements:
            print(movement)
            dir = f'{dir_str}/{movement}/{USED_PAIR_OF_AXIS}'
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
    # i = 0
    # for label in y:
    #     y[i] = movements.index(label)
    #     i += 1

    runs = 5
    previous_score = 0
    for i in range(runs):
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        print(" - Running - ", i)
        for actual_classifier in classifiers:
            classifier = getClassifier(actual_classifier)
            classifier.fit(X_train, y_train)
            if actual_classifier != "MLPClassifier":
                score = classifier.score(X_test, y_test)
                print("    -  ", actual_classifier, score)
                methods_score[actual_classifier] += score
                if score > previous_score:
                    print('   -  highest score = ', score)
                    previous_score = score
                    joblib.dump(classifier, actual_classifier)
            else:
                predictions = classifier.predict(X_test)
                print(confusion_matrix(y_test,predictions))
                print(classification_report(y_test,predictions))

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
