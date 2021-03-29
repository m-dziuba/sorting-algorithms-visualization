import timeit
from sorting_algorithms import *


def test_ss():
    algo = SelectionSort()
    algo.algorithm()


def test_bs():
    algo = BubbleSort()
    algo.algorithm()


def test_is():
    algo = InsertionSort()
    algo.algorithm()


def test_ms():
    algo = MergeSort()
    algo.algorithm()


def test_qs():
    algo = QuickSort()
    algo.algorithm()


def test_cs():
    algo = CountingSort()
    algo.algorithm()


if __name__ == "__main__":
    number = 5
    print(timeit.timeit("test_ss()", setup="from test import test_ss", number=number),
          "SelectionSort")
    print(timeit.timeit("test_bs()", setup="from test import test_bs", number=number),
          "BubbleSort")
    print(timeit.timeit("test_is()", setup="from test import test_is", number=number),
          "InsertionSort")
    print(timeit.timeit("test_ms()", setup="from test import test_ms", number=number),
          "MergeSort")
    print(timeit.timeit("test_qs()", setup="from test import test_qs", number=number),
          "QuickSort")
    print(timeit.timeit("test_cs()", setup="from test import test_cs", number=number),
          "CountingSort")