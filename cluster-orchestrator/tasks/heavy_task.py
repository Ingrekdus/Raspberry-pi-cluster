# tasks/heavy_task.py

import time

{
  "name": "heavy_task",
  "image": "python:3.9-slim",
  "script": "heavy_task.py"
}


def run():
    print("Start výpočtu...")
    result = 0
    for i in range(10**7):  # Těžký výpočet
        result += i ** 0.5
    time.sleep(3)
    print("Hotovo.")
    return result
