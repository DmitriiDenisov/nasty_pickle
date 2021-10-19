import pickle


# 1. Hi bomb: bomb_hi
# 2. Open URL bomb: bomb_open_link
# 3. Open image bomb: bomb_pic
# 4. Swap integers: bomb_swap_integers

def main():
    # unpickle bomb
    with open('bombs_pickles/bomb_pic.pkl', 'rb') as f:
        payload = f.read()
        data = pickle.loads(payload)
        print("Data:", data)

    # print("This is 50:", 50)
    # print("This is 40:", 40)


if __name__ == '__main__':
    main()
