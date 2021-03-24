import numpy as np


def generate_array(max_number, size):

    return [np.random.randint(max_number, size=size)[i] for i in range(size)]


def selection_sort(array):
    for i in range(len(array)):
        min_index = i
        for j in range(i + 1, len(array)):
            if array[min_index] > array[j]:
                min_index = j
        array[i], array[min_index] = array[min_index], array[i]
    return array


def bubble_sort(array):
    swapping = True
    passes = 0
    while swapping:
        swapping = False
        for i in range(len(array) - passes - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapping = True
        passes += 1
    return array


def insertion_sort(array):
    for i in range(1, len(array)):
        for j in range(i - 1, -1, -1):
            if array[i] > array[j]:
                break
            elif array[i] < array[j] and j == 0:
                array.insert(0, array[i])
                del array[i + 1]
            elif array[j] > array[i] >= array[j - 1]:
                array.insert(j, array[i])
                del array[i + 1]

    return array


def merge_sort(array):
    array_length = len(array)
    if array_length > 1:
        first_half = array[:array_length // 2]
        second_half = array[array_length // 2:]
        merge_sort(first_half)
        merge_sort(second_half)

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
    return array


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


if __name__ == '__main__':
    test_case = generate_array(100, 1000)
    # test_case = [67, 46, 14, 14, 10, 83, 11, 93, 10, 15]
    print(test_case)
    sorted_test_case = sorted(test_case)
    sorted_array = quick_sort(test_case)
    print(sorted_array)
    print(sorted_test_case)
    print(sorted_array == sorted_test_case)
