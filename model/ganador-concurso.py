# coding: utf-8
import json

import firebase_admin
from firebase_admin import auth, credentials, db

from datetime import datetime 

INITIAL_DATE = datetime.timestamp(datetime(2021,5,5,23,59,59))
FINAL_DATE = datetime.timestamp(datetime(2021,5,11,23,59,59))

cred = credentials.Certificate('./service-account-file.json')
default_app = firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})

def get_reference(reference_path: str) -> object:
    return db.reference('/' + reference_path)

def count_points(data):
  count = 0
  for movement_type, movement_attempts in data.items():
    for attempt_id, attempt in movement_attempts.items():
      if attempt['timestamp'] > INITIAL_DATE and 
         attempt['timestamp'] < FINAL_DATE and 
         attempt['success']:
        count += 1
  return count

def get_winner():
  ref = get_reference('/users_data')
  users_data = ref.get()

  users_points = {}
  for user_id, data in users_data.items():
    points = count_points(data)
    users_points[user_id] = points
  print(users_points)

get_winner()
