# coding: utf-8
import json
import operator

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
  total = 0
  for movement_type, movement_attempts in data.items():
    for attempt_id, attempt in movement_attempts.items():
      if attempt['timestamp'] > INITIAL_DATE \
        and attempt['timestamp'] < FINAL_DATE:
          if attempt['success']:
            count += 1
          total += 1
  return count, total

def get_user_data(user_id):
  ref = get_reference(f'/users/{user_id}')
  data = ref.get()
  return {'email': data['email'], 'name': data['name']}

def get_winner():
  ref = get_reference('/users_data')
  users_data = ref.get()

  users_points = {}
  total_points = 0
  total_attempts = 0
  for user_id, data in users_data.items():
    if user_id not in ['Circle', 'Infinity', 'Diamond', 'S_Shape', 'Square', 'Triangle']:
      points, total = count_points(data)
      data = get_user_data(user_id)
      users_points[user_id] = {'points': points, 'total': total, 'data': data}
      total_points += points
      total_attempts += total
  
  sorted_users = sorted(users_points.items(), key=lambda x: x[1]['points'], reverse=True)
  print('  Puntos  |    Nombre  ')
  print('-----------------------------------------')
  for user_id, user in sorted_users:
    print(f"    {user['points']:03d}      {user['data']['name']}  - {user['data']['email']} ")

  print("total points = ", total_points)
  print("total attempts = ", total_attempts)

get_winner()
