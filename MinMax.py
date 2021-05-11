#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Objects for retrieving and storing the values and indeces of the arrays
minimum and/or maximum element.

Usage:
To retrieve the values:
- `obj.value`
- `object.index`

To store the values:
- `min = 12`
- `minindex = 0`
- `minobj = Min(12,0)`

To evaluate the min or max:
- `arr = [0,1,2,3,4,5,6,7]`
- `obj = Max()`
- `obj.get(arr)`
"""

import sys

class Min:
    def __init__(self,value=None,index=None):
        self.value = value
        self.index = index
        self.array = []

    def __str__(self):
        return f"<Min object; value: {self.value}, index: {self.index}>"

    def indmin(self):
        return (self.min_index,self.min_value)

    def get(self,arr):
        min_, min_i, n = sys.maxsize, 0, len(arr)
        if n == 0: return
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

class Max:
    def __init__(self,value=None,index=None):
        self.value = value
        self.index = index
        self.array = []

    def __str__(self):
        return f"<Max object; value: {self.value}, index: {self.index}>"

    def indmax(self):
        return (self.max_index,self.max_value)

    def get(self,arr):
        max_, max_i, n = -sys.maxsize, 0, len(arr)
        if n == 0: return
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

class MinMax:
    def __init__(self):
        self.min_value = None
        self.min_index = None
        self.max_value = None
        self.max_index = None
        self.array = None

    def __str__(self):
        return f"<MinMax object>"

    def indminmax(self):
        return ((self.min_value,self.min_index),(self.max_value,self.max_index))


    def get(self,arr):
        max_, max_i, n = -sys.maxsize, 0, len(arr)
        min_, min_i = sys.maxsize, 0
        if n == 0: return
        if n & 1: n -= 1
        for i in range(0,n,2):
            if arr[i+1] > arr[i]:
                maximum, maxindex = arr[i+1], i + 1
                minimum, minindex = arr[i], i
            else:
                minimum, minindex = arr[i+1], i + 1
                maximum, maxindex = arr[i], i
            if maximum > max_: max_, max_i = maximum, maxindex
            if minimum < min_: min_, min_i = minimum, minindex
        if n & 1:
            if arr[n] > max_: max_, max_i = arr[n], n
            if arr[n] < min_: min_, min_i = arr[n], n
        self.array = arr
        self.min_value = min_
        self.max_value = max_
        self.min_index = min_i
        self.max_index = max_i
