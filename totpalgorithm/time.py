import time
import math
from time import sleep

TIME_INTERVAL = 120

def update():
  first_value = time.time()//TIME_INTERVAL
  print("Time left = ", TIME_INTERVAL - math.floor(time.time() % TIME_INTERVAL) )
  count = 0
  while True:
    time.sleep(1)
    print("Time = ", time.time())
    print("Time left = ", TIME_INTERVAL - math.floor(time.time() % TIME_INTERVAL) )
    second_value = time.time()//TIME_INTERVAL
    count += 1
    if second_value != first_value:
      print("Count = ", count)
      print("First = ", first_value)
      print("Second = ", second_value)
      count = 0
      first_value = second_value

update()