# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import itertools
import sys
from pathlib import Path

import firebase_admin
from firebase_admin import auth, credentials, db

cred = credentials.Certificate('./service-account-file.json')
default_app = firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})


def get_reference(reference_path: str) -> object:
    return db.reference('/' + reference_path)


def plot_data(movement, mov_id, matrix):
  combinations = list(itertools.combinations(matrix.keys(), 2))
  fig, axs = plt.subplots(3, 2)
  fig.suptitle(movement)
  i = 0
  j = 0
  for var_1, var_2 in combinations: 
    #axs[i,j].set_ylim([-1, 1])
    #axs[i,j].set_xlim([-1, 1])
    axs[i, j].plot(matrix[var_1], matrix[var_2])
    axs[i, j].set_title(str(var_1)+' vs ' + str(var_2))
    j += 1     
    if j == 2:
      j = 0
      i += 1
    plot2 = plt.figure(2)
    plt.plot(matrix[var_1], matrix[var_2])
    plt.axis('off')
    path = f'./shape/{movement}/{var_1}-{var_2}'
    Path(path).mkdir(parents=True, exist_ok=True)
    plt.savefig(path + f'/{mov_id}.png')
    plt.clf()
    
  plt.tight_layout()
  path = f'./graphs/{movement}/'
  Path(path).mkdir(parents=True, exist_ok=True)
  plt.savefig(path + f'/{mov_id}.png')
  plt.clf()
  """
  plot2 = plt.figure(2)
  plt.plot(matrix['z'], matrix['x'])
  plt.axis('off')
  plt.savefig('./shape/'+movement+'.png')
  """


def run_for_all_data():
  ref = get_reference('/data')
  data = ref.get()
  for movement, value in data.items():
    print('Doing movement ', movement)
    for mov_id, movement_data in data[movement].items():
      plot_data(movement, mov_id, movement_data)
    print('Done with movement ', movement)

run_for_all_data()

