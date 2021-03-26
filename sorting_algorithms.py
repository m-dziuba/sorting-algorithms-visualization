import numpy as np
import random
import time


class Algorithm(object):

    def __init__(self, name):
        self.name = name
        self.start_time = time.time()
        self.time_elapsed = time.time() - self.start_time
        self.array = self.generate_array()

    def generate_array(self):
        self.array = random.sample(range(1024), 1024)
        # self.array = [513, 408, 199, 100, 73, 642, 190, 696]

        self.update_display()
        return self.array

    def run(self):
        return self.array, self.time_elapsed

    def update_display(self):
        import visualizer
        visualizer.update(self.array)


class SelectionSort(Algorithm):

    def __init__(self):
        super(SelectionSort, self).__init__("SelectionSort")

    def print_array(self):
        print(self.array)

    def algorithm(self):
        array_length = len(self.array)
        for i in range(array_length):
            min_index = i
            for j in range(i + 1, len(self.array)):
                if self.array[min_index] > self.array[j]:
                    min_index = j
            self.array[i], self.array[min_index] = self.array[min_index], self.array[i]
            self.update_display()


class BubbleSort(Algorithm):

    def __init__(self):
        super(BubbleSort, self).__init__("BubbleSort")

    def algorithm(self):
        swapping = True
        passes = 0
        while swapping:
            swapping = False
            for i in range(len(self.array) - passes - 1):
                if self.array[i] > self.array[i + 1]:
                    self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                    swapping = True
            passes += 1
            self.update_display()


class InsertionSort(Algorithm):

    def __init__(self):
        super(InsertionSort, self).__init__("BubbleSort")

    def algorithm(self):
        for i in range(1, len(self.array)):
            for j in range(i - 1, -1, -1):
                if self.array[i] > self.array[j]:
                    break
                elif self.array[i] < self.array[j] and j == 0:
                    self.array.insert(0, self.array[i])
                    del self.array[i + 1]
                elif self.array[j] > self.array[i] >= self.array[j - 1]:
                    self.array.insert(j, self.array[i])
                    del self.array[i + 1]
            self.update_display()


class MergeSort(Algorithm):

    def __init__(self):
        super(MergeSort, self).__init__("MergeSort")

    def algorithm(self, start_index=None, end_index=None):
        if start_index is None:
            start_index, end_index = 0, len(self.array)
        if (end_index - start_index) > 1:
            middle_index = (end_index + start_index) // 2
            self.algorithm(start_index, middle_index)
            self.algorithm(middle_index, end_index)
            i = j = 0
            for k in range(start_index, end_index - 1):
                if i + 1 < len(self.array[start_index: end_index]) and j * 2 < len(self.array[start_index: end_index]):
                    if self.array[start_index + i] < self.array[middle_index + j]:
                        i += 1
                    else:
                        self.array.insert(k, self.array[middle_index + j])
                        i += 1
                        j += 1
                        del self.array[middle_index + j]
                    self.update_display()


class QuickSort(Algorithm):

    def __init__(self):
        super(QuickSort, self).__init__("QuickSort")

    def algorithm(self, start_index=None, end_index=None):
        if start_index is None:
            start_index, end_index = 0, len(self.array) - 1
        if end_index - start_index > 0:
            pivot = self.array[end_index]
            i = start_index
            for j in range(start_index, end_index):
                if self.array[j] < pivot:
                    i += 1
                    self.array[i - 1], self.array[j] = self.array[j], self.array[i - 1]
                    self.update_display()
            self.array[i], self.array[end_index] = self.array[end_index], self.array[i]
            self.update_display()

            self.algorithm(start_index, i - 1)
            self.algorithm(i + 1, end_index)


def heap_sort(array):
    return array


def generate_array(max_number, size):

    return [np.random.randint(max_number, size=size)[i] for i in range(size)]


if __name__ == '__main__':

    algo = QuickSort()
    print(algo.array)
    x = sorted(algo.array)
    print(sorted(x))
    algo.algorithm()
    print(algo.array)
    print(algo.array == x)
