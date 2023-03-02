import algorithm


class TestSift:
    def test_one(self):
        assert algorithm.balance("tests/sift_test1.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (8, 5)],
            [(8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (7, 10), (6, 10), (5, 10), (4, 10), (3, 10), (2, 10), (1, 10)],
            [(1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 5), (7, 5)],
            [(7, 5), (7, 4), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3)],
            [(1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (7, 5), (6, 5)],
            [(6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9)],
            [(1, 9), (1, 8), (1, 7), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (5, 5)],
            [(5, 5), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4)],
            [(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 5), (4, 5)],
            [(4, 5), (4, 6), (4, 7), (4, 8), (3, 8), (2, 8), (1, 8)],
            [(1, 8), (1, 7), (1, 6), (2, 6), (3, 6), (4, 6), (4, 5), (3, 5)],
            [(3, 5), (3, 4), (2, 4)],
            [(2, 4), (3, 4), (3, 5), (2, 5)],
            [(2, 5), (2, 6), (2, 7), (1, 7)],
            [(1, 7), (1, 6), (2, 6), (2, 5), (1, 5)],
            [(1, 5), (1, 6)],
            [(1, 6), (1, 5), (2, 5), (3, 5), (3, 4), (2, 4)],
            [(2, 4), (2, 5), (1, 5)]
        ]

    def test_two(self):
        assert algorithm.balance("tests/sift_test2.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (7, 7), (6, 7), (5, 7)],
            [(5, 7), (6, 7), (7, 7), (7, 6), (6, 6)],
            [(6, 6), (6, 7)],
            [(6, 7), (6, 6), (5, 6)],
            [(5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7), (6, 7)],
            [(6, 7), (6, 6), (5, 6)],
            [(5, 6), (6, 6), (6, 7), (5, 7)],
            [(5, 7), (6, 7), (6, 6)],
            [(6, 6), (7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7), (6, 7), (5, 7)],
        ]

    def test_three(self):
        assert algorithm.balance("tests/sift_test3.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6)],
            [(4, 6), (4, 5), (3, 5)],
            [(3, 5), (4, 5), (4, 6), (3, 6)],
            [(3, 6), (3, 7)],
            [(3, 7), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (4, 6), (4, 7)],
            [(4, 7), (4, 6), (3, 6), (2, 6), (1, 6)],
            [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (5, 7)],
            [(5, 7), (5, 6), (5, 5), (4, 5), (3, 5)],
            [(3, 5), (3, 6), (2, 6), (1, 6)],
            [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 7), (5, 7)],
            [(5, 7), (5, 6), (4, 6), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (4, 6), (5, 6), (5, 7), (4, 7)],
            [(4, 7), (4, 6), (3, 6)],
            [(3, 6), (4, 6), (4, 7), (3, 7)],
            [(3, 7), (3, 8)],
            [(3, 8), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (4, 7), (4, 6)],
            [(4, 6), (4, 7), (3, 7), (2, 7), (1, 7)],
            [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (5, 6)],
            [(5, 6), (5, 7), (5, 8), (4, 8), (3, 8)],
            [(3, 8), (3, 7), (2, 7), (1, 7)],
            [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (6, 6), (5, 6)],
            [(5, 6), (5, 7), (4, 7), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (4, 7), (5, 7), (5, 6), (4, 6)],
            [(4, 6), (4, 7), (3, 7)],
            [(3, 7), (4, 7), (4, 6), (3, 6)],
            [(3, 6), (3, 5)],
            [(3, 5), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (4, 6), (4, 5)],
            [(4, 5), (4, 6), (4, 7), (4, 8), (3, 8), (2, 8)],
            [(2, 8), (3, 8), (4, 8), (4, 7), (4, 6), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (4, 6), (5, 6), (5, 5), (4, 5)],
            [(4, 5), (4, 6), (3, 6)],
            [(3, 6), (4, 6), (4, 5), (3, 5)],
            [(3, 5), (4, 5), (4, 6), (4, 7), (4, 8), (3, 8), (2, 8)],
            [(2, 8), (3, 8), (4, 8), (4, 7), (3, 7)],
            [(3, 7), (3, 8)],
            [(3, 8), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (4, 7), (4, 6)],
            [(4, 6), (4, 5), (3, 5), (2, 5)],
            [(2, 5), (3, 5), (4, 5), (5, 5), (5, 6), (5, 7), (4, 7), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (4, 7), (4, 8), (3, 8)],
            [(3, 8), (3, 7), (4, 7), (5, 7), (5, 6), (5, 5), (4, 5), (3, 5), (2, 5)],
            [(2, 5), (3, 5), (4, 5), (5, 5), (5, 6), (4, 6)],
            [(4, 6), (4, 5), (3, 5)],
            [(3, 5), (4, 5), (4, 6), (3, 6)],
            [(3, 6), (3, 7)],
            [(3, 7), (3, 6), (4, 6), (4, 5), (3, 5)],
            [(3, 5), (3, 6)]
        ]

    def test_four(self):
        assert algorithm.balance("tests/sift_test4.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (8, 5)],
            [(8, 5), (8, 6), (8, 7), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7)],
            [(1, 7), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 5), (7, 5)],
            [(7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7)],
            [(2, 7), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (7, 5), (6, 5)],
            [(6, 5), (6, 6), (6, 7), (5, 7), (4, 7), (3, 7)],
            [(3, 7), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (5, 5)],
            [(5, 5), (5, 6), (5, 7), (4, 7)],
            [(4, 7), (4, 6), (5, 6), (5, 5), (4, 5)],
            [(4, 5), (4, 6), (5, 6), (5, 7), (5, 8), (4, 8), (3, 8), (2, 8)],
            [(2, 8), (3, 8), (4, 8), (5, 8), (5, 7), (5, 6), (5, 5), (4, 5), (3, 5)],
            [(3, 5), (3, 6), (4, 6), (5, 6), (5, 7), (5, 8), (4, 8), (3, 8)],
            [(3, 8), (4, 8), (5, 8), (5, 7), (5, 6), (5, 5), (4, 5), (3, 5), (2, 5)],
            [(2, 5), (2, 6), (1, 6)],
            [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (5, 7), (4, 7)],
            [(4, 7), (4, 8)],
            [(4, 8), (4, 7), (3, 7)],
            [(3, 7), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (3, 6), (3, 5), (2, 5)],
            [(2, 5), (3, 5), (3, 6), (3, 7), (2, 7), (1, 7)],
            [(1, 7), (2, 7), (3, 7), (3, 6), (3, 5)],
            [(3, 5), (3, 6), (3, 7), (4, 7), (5, 7), (5, 8), (4, 8)],
            [(4, 8), (4, 7), (3, 7), (2, 7), (1, 7)],
            [(1, 7), (2, 7), (3, 7), (3, 6), (4, 6), (4, 5), (3, 5)],
            [(3, 5), (3, 6), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (4, 7), (4, 8), (3, 8)],
            [(3, 8), (3, 7), (3, 6)]
        ]

    def test_five(self):
        assert algorithm.balance("tests/sift_test5.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (8, 7), (7, 7), (6, 7), (5, 7), (4, 7)],
            [(4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (8, 6), (7, 6)],
            [(7, 6), (7, 7), (6, 7), (5, 7)],
            [(5, 7), (6, 7), (7, 7), (7, 6), (6, 6)],
            [(6, 6), (6, 7)],
            [(6, 7), (6, 6), (5, 6)],
            [(5, 6), (6, 6), (7, 6), (7, 7)],
            [(7, 7), (7, 6), (6, 6), (5, 6), (4, 6)],
            [(4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 7)],
            [(8, 7), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (3, 6)],
            [(3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7)],
            [(8, 7), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (3, 6)],
            [(3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 7), (7, 7)],
            [(7, 7), (7, 6), (6, 6), (5, 6), (4, 6)],
            [(4, 6), (5, 6), (6, 6), (7, 6), (7, 7), (6, 7)],
            [(6, 7), (6, 6), (5, 6)],
            [(5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6)]
        ]

    def test_six(self):
        assert algorithm.balance("tests/sift_test6.txt") == []


class TestBalance:
    def test_one(self):
        assert algorithm.balance("tests/balance_test1.txt") == [
            [(9, 1), (9, 2), (9, 3), (8, 3), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3)],
            [(1, 3), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (1, 7)],
            [(1, 7), (1, 6), (1, 5), (2, 5), (2, 4), (1, 4)],
            [(1, 4), (1, 5), (1, 6), (2, 6), (2, 7)]
        ]

    def test_two(self):
        assert algorithm.balance("tests/balance_test2.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6)],
            [(6, 6), (6, 7), (5, 7)],
            [(5, 7), (6, 7), (6, 6), (7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6)]
        ]

    def test_three(self):
        assert algorithm.balance("tests/balance_test3.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6)],
            [(4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 7)]
        ]

    def test_four(self):
        assert algorithm.balance("tests/balance_test4.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6)],
            [(4, 6), (4, 7), (3, 7), (2, 7), (1, 7)],
            [(1, 7), (2, 7), (3, 7), (4, 7), (4, 6), (3, 6)],
            [(3, 6), (3, 7), (2, 7)],
            [(2, 7), (3, 7), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (3, 7)],
            [(3, 7), (3, 6), (2, 6), (1, 6)],
            [(1, 6), (2, 6), (3, 6), (4, 6), (4, 7)]
        ]

    def test_five(self):
        assert algorithm.balance("tests/balance_test5.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7)],
            [(8, 7), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-5, -23), (-4, -23), (-3, -23), (-2, -23), (-1, -23)],
            [(-1, -23), (-2, -23), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-5, -23), (-5, -22), (-4, -22), (-3, -22), (-2, -22), (-1, -22)],
            [(-1, -22), (-2, -22), (-2, -23), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7)],
            [(7, 7), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7)],
            [(7, 7), (8, 7), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-5, -23), (-4, -23), (-3, -23), (-2, -23), (-1, -23)],
            [(-1, -23), (-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-5, -23), (-5, -22), (-4, -22), (-3, -22), (-2, -22), (-1, -22)],
            [(-1, -22), (-1, -23), (-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7)]
        ]

    def test_six(self):
        assert algorithm.balance("tests/balance_test6.txt") == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6)],
            [(2, 6), (3, 6), (3, 7)],
            [(3, 7), (3, 6), (3, 5), (4, 5), (4, 4), (5, 4), (5, 3), (6, 3), (6, 2), (5, 2)],
            [(5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (4, 7)],
            [(4, 7), (4, 6), (4, 5), (4, 4), (5, 4), (5, 3), (5, 2), (6, 2), (7, 2), (8, 2), (8, 1), (7, 1)],
            [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7)],
            [(5, 7), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (6, 2), (7, 2), (7, 1), (6, 1)],
            [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]
        ]


class TestLoadUnload:
    def test_one(self):
        assert algorithm.load_unload("tests/load_unload_test1.txt", ["CONTAINER5", "CONTAINER6"], [(1, 1), (1, 11)]) == [
            [(9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1)],
            [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (0, 0)],
            ['CONTAINER6', (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1)],
            [(1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 10), (3, 11), (2, 11)],
            [(2, 11), (2, 10), (1, 10)],
            [(1, 10), (2, 10), (2, 11), (1, 11)],
            [(1, 11), (2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (0, 0)],
            ['CONTAINER5', (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1)]
        ]

    def test_two(self):
        assert algorithm.load_unload("tests/load_unload_test2.txt", ["CONTAINER1", "CONTAINER1"], []) == [
            [(9, 1), (0, 0)],
            ['CONTAINER1', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER1', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)]
        ]

    def test_three(self):
        assert algorithm.load_unload("tests/load_unload_test3.txt", ["CONTAINER5", "CONTAINER6", "CONTAINER7", "CONTAINER8"], [(7, 6), (7, 7), (8, 6), (8, 7)]) == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            [(0, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER8', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 7), (8, 7)],
            [(8, 7), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER7', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (8, 7), (7, 7)],
            [(7, 7), (8, 7), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER6', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7)],
            [(7, 7), (8, 7), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER5', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7)]
        ]

    def test_four(self):
        assert algorithm.load_unload("tests/load_unload_test3.txt", ["CONTAINER5", "CONTAINER6"], [(7, 6), (7, 7)]) == [
            [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER6', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 7), (8, 7)],
            [(8, 7), (8, 6)],
            [(8, 6), (8, 7), (7, 7)],
            [(7, 7), (8, 7), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER5', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7)],
            [(7, 7), (8, 7), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (-5, -24), (-4, -24), (-3, -24), (-2, -24), (-1, -24)],
            [(-1, -24), (-2, -24), (-3, -24), (-4, -24), (-5, -24), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7)]
        ]

    def test_five(self):
        assert algorithm.load_unload("tests/load_unload_test4.txt", ["CONTAINER1", "CONTAINER2", "CONTAINER3", "CONTAINER4"], []) == [
            [(9, 1), (0, 0)],
            ['CONTAINER4', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6), (6, 6)],
            [(6, 6), (7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER3', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6), (7, 6)],
            [(7, 6), (8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER2', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (8, 6)],
            [(8, 6), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (0, 0)],
            ['CONTAINER1', (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (8, 7), (7, 7), (6, 7)]
        ]
