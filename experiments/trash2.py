import pickle

with open('../bombs/bomb_hi.pkl', 'rb') as read_file:
    new_noise = pickle.load(read_file)

with open('../bombs/bomb_virus_with_pic.pkl', 'rb') as f:
    payload = f.read()
    data = pickle.loads(payload)
    print(data)


# --------------------
# Не открывает картинку
with open('../filename.pickle', 'wb') as handle:
    pickle.dump(['A', 'B'], handle)

with open('../filename.pickle', 'rb') as handle:
    data4 = pickle.load(handle)
print(data4)
