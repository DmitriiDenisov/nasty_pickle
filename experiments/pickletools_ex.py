# import pickle
import pickle
import pickletools

payload = pickle.dumps(["aaa", 111])
payload = pickletools.optimize(payload)

pickletools.dis(payload)
