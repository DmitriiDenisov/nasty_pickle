import pickle


def main():
    # unpickle bomb
    with open('bombs_pickles/bomb_swap_integers.pkl', 'rb') as f:
        payload = f.read()
        data = pickle.loads(payload)
        print("Data:", data)

    print("This is 50:", 50)
    print("This is 40:", 40)


if __name__ == '__main__':
    main()
