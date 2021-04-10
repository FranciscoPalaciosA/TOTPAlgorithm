# coding: utf-8
import io
import itertools
import os.path
import sys
from pathlib import Path

import cv2
import firebase_admin
import matplotlib.pyplot as plt
import numpy as np
from firebase_admin import auth, credentials, db
from matplotlib.figure import Figure

cred = credentials.Certificate('./service-account-file.json')
default_app = firebase_admin.initialize_app(credential=cred, options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})


def get_reference(reference_path: str) -> object:
    return db.reference('/' + reference_path)


def compress_matrix(matrix):
    h, w = matrix.shape
    new_h = int(h / 4)
    new_w = int(w / 4)
    jump = 4

    compressed_matrix = np.zeros((new_h, new_w))
    for i in range(new_h):
        for j in range(new_w):
            nums_to_avg = []
            for k in range(4):
                for l in range(4):
                    nums_to_avg.append(matrix[i * jump + k][j * jump + l])
            compressed_matrix[i][j] = get_avg(nums_to_avg)
    return compressed_matrix

def get_avg(arr):
    s = 0
    for i in arr:
        s = s + i
    return 255 -  s / len(arr)

def plot_data(movement, mov_id, matrix):
  combinations = list(itertools.combinations(matrix.keys(), 2))
  i = 0
  j = 0
  for var_1, var_2 in combinations: 
    j += 1     
    if j == 2:
      j = 0
      i += 1

    fig = Figure()
    ax = fig.subplots()
    ax.plot(matrix[var_1], matrix[var_2])
    ax.axis('off')

    # Write img matrix in memory
    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw')
    io_buf.seek(0)
    img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                        newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
    io_buf.close()

    # Change to gray 
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    compressed_matrix = compress_matrix(gray)

    path = f'./compress/shape/{movement}/{var_1}-{var_2}'
    Path(path).mkdir(parents=True, exist_ok=True)
    
    # Save image
    cv2.imwrite(path + f'/{mov_id}.png', compressed_matrix)
    plt.clf()


def run_for_all_data():
  ref = get_reference('/data')
  data = ref.get()
  for movement, value in data.items():
    print('Doing movement ', movement)
    for mov_id, movement_data in data[movement].items():
      if not (os.path.exists(f'.compress/shape/{movement}/w-x/{mov_id}.png')): #If its in one it should be in all
        print('   Doing mov_id ', mov_id)
        if isinstance(movement_data, dict):
          plot_data(movement, mov_id, movement_data)
    print('Done with movement ', movement)

run_for_all_data()

