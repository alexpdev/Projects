import sys
from unittest import TestCase
from time import time
from random import randint
from string import ascii_letters
import typing

def max_get(arr) -> list:
    """
    ### max_get
    Get array element and index with maximum value.

    - Args:
        `arr` list/dict/tuple/set: any seq that supports __contains__.

    - Returns:
        `(int,int) : (max_value, max_index)`
    """
    max_, max_i, n = -sys.maxsize, 0, len(arr)
    if n == 0: return
    if n & 1: n -= 1
    for i in range(0,n,2):
        if arr[i+1] > arr[i]: maximum, index = arr[i+1], i+1
        else: maximum, index = arr[i], i
        if maximum > max_: max_, max_i = maximum, index
    if n & 1:
        if arr[n] > max_: max_, max_i = arr[n], n
    return (max_,max_i)

def min_get(arr) -> list:
    """
    ### min_get
    Get array element and index with maximum value.

    - Args:
        `arr` list/dict/tuple/set: any seq that supports __contains__.

    - Returns:
        (int,int) (min_value, min_index)
    """
    min_, min_i, n = sys.maxsize, 0, len(arr)
    if n == 0: return
    if n & 1: n -= 1
    for i in range(0,n,2):
        if arr[i+1] < arr[i]: minimum, index = arr[i+1], i+1
        else: minimum, index = arr[i], i
        if minimum < min_: min_, min_i = minimum, index
    if n & 1:
        if arr[n] < min_: min_, min_i = arr[n], n
    return (min_, min_i)

def minmax_get(arr) -> list:
    """
    ### minmax_get
    - Description: Get value and index of maximum element and minimum elements in array.

    - Args:
        arr ([list/tuple/set/dict]): Any seq type structure that supports contains function.

    - Returns:
        `(int,int),(int,int)`: `(max_value,max_index),(min_value,min_index)`
    """
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
    return [(max_,max_i),(min_,min_i)]
