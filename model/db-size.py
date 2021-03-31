# coding: utf-8
import json
import os
import os.path

import firebase_admin
from firebase_admin import auth, credentials, db

cred = credentials.Certificate('./service-account-file.json')
default_app = firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})


def get_reference(reference_path: str) -> object:
    return db.reference('/' + reference_path)


def measure_db():
  """
  Comment the next lines if your db.json is updated
  """
  ref = get_reference('/data')
  data = ref.get()
  print(data, file=open("db.json", "a"))

  """
  Uncomment the next two lines if your db.json is updated
  f = open('./db.json',)
  data = json.load(f)
  """

  print('\n--- From DB ---')
  for movement, value in data.items():
    print(f'{movement} sample size = {len(value)}')

  print('\n--- From Local files --- ')
  print('----- Graphs ----- ')
  movements = sorted(os.listdir('./graphs'))
  for movement in movements:
    if movement != '.DS_Store':
      print(
        movement +
        " - " + 
        str(
          len(
            [name for name in os.listdir(f'./graphs/{movement}') if os.path.isfile(f'./graphs/{movement}/{name}')]
            )
          )
      )
  print('----- Shapes ----- ')
  shape_movements = sorted(os.listdir('./shape'))
  for movement in shape_movements:
    if movement != '.DS_Store':
      pair_of_vars = sorted(os.listdir(f'./shape/{movement}'))
      print(' * ' + movement)
      for pair in pair_of_vars:
        if pair != '.DS_Store':
          print(
            pair +
            " - " + 
            str(
              len(
                [name for name in os.listdir(f'./shape/{movement}/{pair}') if os.path.isfile(f'./shape/{movement}/{pair}/{name}')]
                )
              )
          )
        

  

measure_db()
