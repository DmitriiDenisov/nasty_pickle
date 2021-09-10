import pickle

from random import randint
rand = randint(0, 1)
if rand:
    print("Generated 1")
else:
    print("Generated 1")

for i in range(1, 10):
    print(i)
    try:
        a = i
    except ZeroDivisionError:
        a = 2