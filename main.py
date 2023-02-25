import algorithm


def main():
    moves = algorithm.balance("tests/balance_test6.txt")
    for move in moves:
        print(move)


if __name__ == "__main__":
    main()
