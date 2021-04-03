import os
import cv2
import joblib

USED_PAIR_OF_AXIS = 'x-z'
ITEMS_PER_MOVEMENT = 2
CLASSIFIER = 'RandomForestClassifier'

model = joblib.load(f'./{CLASSIFIER}')

movements = [
        'Circle',
        'Triangle',
        'Infinity',
        'Square',
        'S_Shape',
        'Diamond'
        ]

print(model.classes_)

for movement in movements:
    dir = f'./shape/{movement}/{USED_PAIR_OF_AXIS}'
    i = 0
    print(f'Movement: {movement}')
    for filename in os.listdir(dir):
        if filename != '.DS_Store':
            if i >= ITEMS_PER_MOVEMENT:
                break
            i += 1
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                img = cv2.imread(f)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).reshape(1,-1)
                f = open(f'./tests/jsons/{movement}_{str(i)}.json', "w")
                # for el in list(gray[0]):
                #     print(el)
                f.write(f'{list(gray[0])}')
                f.close()
                print(model.predict(gray)[0], model.predict_proba(gray))

