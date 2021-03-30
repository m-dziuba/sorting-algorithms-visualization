import random
import time


class Algorithm:
    def __init__(self, name):
        self.name = name
        self.start_time = time.time()
        self.time_elapsed = time.time() - self.start_time
        self.array = random.sample(range(1024), 128)
        self.array_length = len(self.array)
        self.bar_width = 1024 // self.array_length

    def generate_array(self):
        self.array = random.sample(range(1024), 128)
        # self.array = [513, 408, 199, 100, 73, 642, 190, 696]
        self.array_length = len(self.array)
        self.bar_width = 1024 // self.array_length
        self.update_display()
        return self.array

    def set_start_time(self):
        self.start_time = time.time()

    def update_display(self, start=0, end=128, inspected=None, compared=(None, None)):
        import visualizer
        self.time_elapsed = time.time() - self.start_time
        visualizer.check_events(self, None)
        visualizer.update(self.array, self.bar_width, start, end, inspected, compared, self.time_elapsed)

    def update_one_bar(self, bar=None, mode=None):
        import visualizer
        self.time_elapsed = time.time() - self.start_time
        visualizer.check_events(self, None)
        visualizer.update_one_bar(bar, self.array, self.bar_width, mode, self.time_elapsed)


class SelectionSort(Algorithm):

    def __init__(self):
        super(SelectionSort, self).__init__("SelectionSort")

    def algorithm(self):
        for i in range(self.array_length):
            min_index = i
            self.update_one_bar(i - 1)
            self.update_one_bar(i, "inspected")
            for j in range(i + 1, self.array_length):
                self.update_one_bar(j - 1 if j - 1 > i else j)
                self.update_one_bar(j, "compared")
                if self.array[min_index] > self.array[j]:
                    min_index = j
            self.array[i], self.array[min_index] = self.array[min_index], self.array[i]
            self.update_one_bar(self.array_length - 1)
            self.update_one_bar(i)
            self.update_one_bar(min_index)


class BubbleSort(Algorithm):

    def __init__(self):
        super(BubbleSort, self).__init__("BubbleSort")

    def algorithm(self):
        swapping = True
        passes = 0
        while swapping:
            swapping = False
            for i in range(self.array_length - passes - 1):
                self.update_one_bar(i, "inspected")
                self.update_one_bar(i + 1, "compared")
                if self.array[i] > self.array[i + 1]:
                    self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                    swapping = True
                self.update_one_bar(i)
                self.update_one_bar(i + 1, "compared")
            self.update_one_bar(self.array_length - passes - 1)
            passes += 1


class InsertionSort(Algorithm):

    def __init__(self):
        super(InsertionSort, self).__init__("BubbleSort")

    def algorithm(self):
        for i in range(1, self.array_length):
            self.update_one_bar(i, "inspected")
            for j in range(i - 1, -1, -1):
                self.update_one_bar(j + 1 if j + 1 != i else j)
                self.update_one_bar(j, "compared")
                if self.array[i] > self.array[j]:
                    self.update_one_bar(j)
                    break
                elif self.array[j] > self.array[i] and j == 0:
                    self.array.insert(j, self.array[i])

                    del self.array[i + 1]
                elif self.array[j] > self.array[i] >= self.array[j - 1]:
                    self.array.insert(j, self.array[i])
                    del self.array[i + 1]
                self.update_one_bar(j)
                self.update_one_bar(j - 1, "compared")


class MergeSort(Algorithm):

    def __init__(self):
        super(MergeSort, self).__init__("MergeSort")

    def algorithm(self, start_index=None, end_index=None):
        if start_index is None:
            start_index, end_index = 0, self.array_length
        if (end_index - start_index) > 1:
            middle_index = (end_index + start_index) // 2
            self.algorithm(start_index, middle_index)
            self.algorithm(middle_index, end_index)
            i = j = 0
            for k in range(start_index, end_index):
                self.update_one_bar(k, "inspected")
                if i + 1 < len(self.array[start_index: end_index]) and j * 2 < len(self.array[start_index: end_index]):
                    self.update_one_bar(middle_index + j, "compared")
                    if self.array[start_index + i] < self.array[middle_index + j]:
                        i += 1
                    else:
                        self.array.insert(k, self.array[middle_index + j])
                        i += 1
                        j += 1
                        del self.array[middle_index + j]
                        self.update_display(k, middle_index + j)
                self.update_one_bar(k)


class QuickSort(Algorithm):

    def __init__(self):
        super(QuickSort, self).__init__("QuickSort")

    def algorithm(self, start_index=None, end_index=None):
        if start_index is None:
            start_index, end_index = 0, self.array_length - 1
        if end_index - start_index > 0:
            pivot = self.array[end_index]
            self.update_one_bar(end_index, "inspected")
            i = start_index
            for j in range(start_index, end_index):
                self.update_one_bar(j, "compared")
                self.update_one_bar(i, "compared")
                if self.array[j] < pivot:
                    i += 1
                    self.array[i - 1], self.array[j] = self.array[j], self.array[i - 1]
                self.update_one_bar(i - 1)
                self.update_one_bar(j)
            self.array[i], self.array[end_index] = self.array[end_index], self.array[i]
            self.update_one_bar(i)
            self.update_one_bar(end_index)
            self.algorithm(start_index, i - 1)
            self.algorithm(i + 1, end_index)


class CountingSort(Algorithm):
    
    def __init__(self):
        super(CountingSort, self).__init__("CountingSort")

    def algorithm(self):
        max_number = 0
        self.update_display()
        for i in self.array:
            if i > max_number:
                max_number = i

        counting_range = [0] * (max_number + 1)
        for i in range(self.array_length):
            self.update_one_bar(i - 1)
            self.update_one_bar(i, "inspected")
            counting_range[self.array[i]] += 1
        self.update_display(self.array_length)
        k = 0
        for i in range(len(counting_range)):
            if counting_range[i] != 0:
                for j in range(counting_range[i]):
                    self.array[k] = i
                    self.update_one_bar(k - 1)
                    self.update_one_bar(k, "inspected")
                    k += 1


if __name__ == '__main__':
    pass
    # algo = SelectionSort()

    # x = sorted(algo.array)
    # print(sorted(x))
    # algo.algorithm()
    # print(algo.array)
    # print(algo.array == x)
