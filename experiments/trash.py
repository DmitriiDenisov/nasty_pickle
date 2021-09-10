import pickle

with open('../bombs/bomb_if_bomb.pkl', 'rb') as f:
    payload = f.read()
    new_noise = pickle.loads(payload)
print(new_noise)

a = 3


