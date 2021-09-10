import pickle


def main():
    # unpickle bomb
    with open('bombs/bomb_self_report.pkl', 'rb') as f:
        payload = f.read()
        data = pickle.loads(payload)
        print(data)

    data2 = [23, 13, 39]

    payload = pickle.dumps(data2)
    data3 = pickle.loads(payload)

    print(data3)


if __name__ == '__main__':
    main()
