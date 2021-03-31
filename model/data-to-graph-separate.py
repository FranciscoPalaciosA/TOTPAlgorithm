# coding: utf-8
import itertools
import os.path
import sys
from pathlib import Path

import firebase_admin
import matplotlib.pyplot as plt
import numpy as np
from firebase_admin import auth, credentials, db

cred = credentials.Certificate('./service-account-file.json')
default_app = firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})


def get_reference(reference_path: str) -> object:
    return db.reference('/' + reference_path)


def plot_data(movement, mov_id, matrix):
  combinations = list(itertools.combinations(matrix.keys(), 2))
  i = 0
  j = 0
  for var_1, var_2 in combinations: 
    j += 1     
    if j == 2:
      j = 0
      i += 1
    plt.plot(matrix[var_1], matrix[var_2])
    plt.axis('off')
    path = f'./shape/{movement}/{var_1}-{var_2}'
    Path(path).mkdir(parents=True, exist_ok=True)
    plt.savefig(path + f'/{mov_id}.png')
    plt.clf()
    

def run_for_all_data():
  ref = get_reference('/data')
  data = ref.get()
  for movement, value in data.items():
    print('Doing movement ', movement)
    for mov_id, movement_data in data[movement].items():
      if not (os.path.exists(f'./shape/{movement}/w-x/{mov_id}.png')): #If its in one it should be in all
        print('   Doing mov_id ', mov_id)
        plot_data(movement, mov_id, movement_data)
    print('Done with movement ', movement)

run_for_all_data()

