import pickle
import pickletools


class MyClass:
    pass


payload = pickle.dumps(MyClass(), protocol=0)
payload = pickletools.optimize(payload)
pickletools.dis(payload)
