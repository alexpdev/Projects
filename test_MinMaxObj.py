import pytest
from random import randint
from MinMaxObj import Min, Max, MinMax

def test_min_class():
    for i in range(100):
        value = randint(-100,100)
        index = randint(0,100)
        obj = Min(value,index)
        assert obj.value == value
        assert obj.index == index

def test_max_class():
    for i in range(100):
        value = randint(-100,100)
        index = randint(0,100)
        obj = Max(value,index)
        assert obj.value == value
        assert obj.index == index

def test_min_function():
    for arr in gen_arrays():
        obj = Min()
        obj.get(arr)
        assert obj.array == arr
        minimum = min(arr)
        assert obj.value == minimum
        min_i = arr.index(minimum)
        assert obj.index == min_i

def test_max_function():
    for arr in gen_arrays():
        obj = Max()
        obj.get(arr)
        assert obj.array == arr
        maximum = max(arr)
        assert obj.value == maximum
        max_i = arr.index(maximum)
        assert obj.index == max_i

def test_minmax_function():
    for arr in gen_arrays():
        obj = MinMax()
        obj.get(arr)
        assert obj.array == arr
        min1,max1 = min(arr),max(arr)
        print(min1,max1)
        assert obj.minimum == min1
        assert obj.maximum == max1
        minIndex,maxIndex = arr.index(min1), arr.index(max1)
        print(minIndex,maxIndex)
        assert obj.minindex == minIndex
        assert obj.maxindex == maxIndex



def gen_arrays(start=10,stop=350,step=8):
    for x in range(start,stop,step):
        yield [randint(-300,300) for i in range(x)]
