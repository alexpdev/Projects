import sys

class Min:
    def __init__(self,value=None,index=None):
        self.value = value
        self.index = index
        self.array = []

    def get(self,arr):
        min_, min_i, n = sys.maxsize, 0, len(arr)
        if n & 1: n -= 1
        for i in range(0,n,2):
            if arr[i+1] < arr[i]:
                minimum, index = arr[i+1], i+1
            else:
                minimum, index = arr[i], i
            if minimum < min_:
                min_, min_i = minimum, index
        if n & 1:
            if arr[n] < min_: min_, min_i = arr[n], n
        self.array = arr
        self.index = min_i
        self.value = min_
        return self


class Max:
    def __init__(self,value=None,index=None):
        self.value = value
        self.index = index
        self.array = []

    def get(self,arr):
        max_, max_i, n = -sys.maxsize, 0, len(arr)
        if n & 1: n -= 1
        for i in range(0,n,2):
            if arr[i+1] > arr[i]:
                maximum, index = arr[i+1], i+1
            else:
                maximum, index = arr[i], i
            if maximum > max_:
                max_, max_i = maximum, index
        if n & 1:
            if arr[n] > max_:
                maximum, max_i = arr[n], n
        self.array = arr
        self.index = max_i
        self.value = max_
        return self

class MinMax:
    def __init__(self):
        self.minimum = None
        self.minindex = None
        self.maximum = None
        self.maxindex = None
        self.array = None

    def get(self,arr):
        max_, max_i, n = -sys.maxsize, 0, len(arr)
        min_, min_i = sys.maxsize, 0
        if n & 1:
            n -= 1
        for i in range(0,n,2):
            if arr[i+1] > arr[i]:
                maximum, maxindex = arr[i+1], i + 1
                minimum, minindex = arr[i], i
            else:
                minimum, minindex = arr[i+1], i + 1
                maximum, maxindex = arr[i], i
            if maximum > max_:
                max_, max_i = maximum, maxindex
            if minimum < min_:
                min_, min_i = minimum, minindex
        if n & 1:
            if arr[n] > max_:
                max_, max_i = arr[n], n
            if arr[n] < min_:
                min_, min_i = arr[n], n
        self.array = arr
        self.minimum = min_
        self.maximum = max_
        self.minindex = min_i
        self.maxindex = max_i
