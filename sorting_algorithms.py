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
        self.array = random.sample(range(800), 512)
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


    def algorithm(self, array=None):
        if not array:
            array = self.array
        array_length = len(array)
        if array_length > 1:
            first_half = array[:array_length // 2]
            second_half = array[array_length // 2:]
            self.algorithm(first_half)
            self.algorithm(second_half)

            i = j = 0
            for k in range(len(array)):
                if i < len(first_half) and j < len(second_half):
                    if first_half[i] < second_half[j]:
                        array[k] = first_half[i]
                        i += 1
                    else:
                        array[k] = second_half[j]
                        j += 1
                elif i < len(first_half):
                    array[k] = first_half[i]
                    i += 1
                elif j < len(second_half):
                    array[k] = second_half[j]
                    j += 1


def quick_sort(array):
    if array:
        pivot = array[len(array) - 1]
        i = - 1
        for j in range(0, len(array) - 1 + 1):
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[len(array) - 1] = array[len(array) - 1], array[i + 1]
        array[:i + 1] = quick_sort(array[:i + 1])
        array[i + 2:] = quick_sort(array[i + 2:])
    return array


def heap_sort(array):
    return array


def generate_array(max_number, size):

    return [np.random.randint(max_number, size=size)[i] for i in range(size)]


if __name__ == '__main__':

    test_case = generate_array(100, 1000)
    # test_case = [67, 46, 14, 14, 10, 83, 11, 93, 10, 15]
    print(test_case)
    sorted_test_case = sorted(test_case)
    sorted_array = quick_sort(test_case)
    print(sorted_array)
    print(sorted_test_case)
    print(sorted_array == sorted_test_case)
