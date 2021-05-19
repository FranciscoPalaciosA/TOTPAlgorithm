# coding: utf-8
from pathlib import Path

import firebase_admin
import numpy as np
from firebase_admin import auth, credentials, db

cred = credentials.Certificate('./service-account-file.json')
default_app = firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})


def get_reference(reference_path: str) -> object:
    return db.reference('/' + reference_path)

def get_success_by_shape():
  ref = get_reference('/attempts_by_shape')
  data = ref.get()
  for movement_name, value in data.items():
    total_attempts = 0
    success_attempts = 0
    for attempt_id, attempt_outcome in value.items():
      total_attempts +=1
      if attempt_outcome:
        success_attempts +=1
    print(f"{movement_name}: success ratio {success_attempts/total_attempts * 100}%  - total {total_attempts}  - {success_attempts}")

def get_avg_model_time():
  ref = get_reference('/sequence_timing')
  data = ref.get()
  total_attempts = 0
  total_time_ms = 0
  for attempt, ms in data.items():
    total_attempts += 1
    total_time_ms += ms['ms']
  print(f"Avg time: {total_time_ms/total_attempts} ms")

def get_complete_success_ratio():
  ref = get_reference('/users')
  data = ref.get()
  total_attempts = 0
  success_attempts = 0
  for user_id, value in data.items():
    if 'attempts' in value:
      print(f'Doing user {user_id}')
      for attempt_category, attempts in value['attempts'].items():
        for attempt_id, attempt in attempts.items():
          if attempt_category == 'success':
            success_attempts += 1
          total_attempts += 1
  print('total attempts = ', total_attempts)
  print('success attempts = ', success_attempts)

def get_sus_score():
  ref = get_reference('/users')
  data = ref.get()
  for user_id, value in data.items():
    if 'survey' in value:
      print(f'User {value["email"]} - {value["survey"]["question1"]}, {value["survey"]["question2"]}, {value["survey"]["question3"]}, {value["survey"]["question4"]}, {value["survey"]["question5"]}, {value["survey"]["question6"]}, {value["survey"]["question7"]}, {value["survey"]["question8"]}, {value["survey"]["question9"]}, {value["survey"]["question10"]} ')
      print(f'{value["survey"]["sum"]} - {value["survey"]["total"]}')
get_success_by_shape()
get_avg_model_time()
get_complete_success_ratio()
get_sus_score()
