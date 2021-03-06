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
    return 255 - s / len(arr)


def plot_data(movement, mov_id, matrix, success):
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

    attempt = 'incorrect'
    if(success):
      attempt = 'correct'

    path = f'./users_shapes/{attempt}/{movement}/{var_1}-{var_2}'
    Path(path).mkdir(parents=True, exist_ok=True)
    
    # Save image
    cv2.imwrite(path + f'/{mov_id}.png', compressed_matrix)
    plt.clf()


def get_data():
  data = get_reference("/users_data").get()
  for user_id, value in data.items():
    print(f"Doing user {user_id}")
    for shape_movement, attemps in value.items():
      for attempt_id, attempt_data in attemps.items():
        print(f"    Doing movement {attempt_id} ")
        plot_data(shape_movement, attempt_id, attempt_data['data'], attempt_data['success'])
    print("Done")

  

get_data()

