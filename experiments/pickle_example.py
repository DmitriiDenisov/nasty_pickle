import pickle

a = {'hello': 'world'}

# Save to file
with open('filename.pickle', 'wb') as handle:
    pickle.dump(a, handle)

# Read from file
with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

print(a == b)