import json

with open('./movementauth-default-rtdb-export.json') as f:
  data = json.load(f)

data = data['data']

circles = data['Circle']
squares = data['Square']

f = open('points.txt','a')

for circleKey in circles:
    f.write(f'{circleKey}\n')
    circle = circles[circleKey]
    w = circle['w']
    x = circle['x']
    y = circle['y']
    z = circle['z']
    for i in range(0,len(w)):
        f.write(f'({x[i]},{y[i]},{z[i]})\n')

f.close()

