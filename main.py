import algorithm


def main():
    moves = algorithm.balance("tests/sift_test6.txt")
    total_time = 0
    for move in moves:
        total_time+=len(move)
        print(move)

    print(total_time)


if __name__ == "__main__":
    main()
