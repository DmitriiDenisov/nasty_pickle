# 1. Create object
class Bomb:
    def __init__(self, name):
        self.name = name

    def __getstate__(self):
        return self.name

    def __setstate__(self, state):
        self.name = state
        print(f'Bang! From, {self.name}.')


bomb = Bomb('Evan')

# 2. Pickle it
import pickle
pickled_bomb = pickle.dumps(bomb, protocol=0)
unpickled_bomb = pickle.loads(pickled_bomb)
print(unpickled_bomb)  # print and see what is inside

# 3. disassembling a pickle
import pickletools
pickletools.dis(pickled_bomb)
print('-' * 50)

# 4. Optimize = removes unused opcodes from the pickle, so it will produce a simpler—but otherwise equivalent—pickle
pickled_bomb = pickletools.optimize(pickled_bomb)
pickletools.dis(pickled_bomb)

# 5. Eval func OR exec
eval("print('Bang! From, Evan')")
print('-' * 50)

# 6. Naive example
pickled_bomb = b'c__builtin__\nexec\n(Vprint("Bang! From, Evan.")\ntR.'
pickle.loads(pickled_bomb)