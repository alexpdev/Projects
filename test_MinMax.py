import pytest
from random import randint
from MinMax import Min, Max, MinMax

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
        assert obj.min_value == min1
        assert obj.max_value == max1
        minIndex,maxIndex = arr.index(min1), arr.index(max1)
        assert obj.min_index == minIndex
        assert obj.max_index == maxIndex

def test_empty_array():
    arr = []
    minobj = Min()
    maxobj = Max()
    minobj.get(arr)
    maxobj.get(arr)
    assert minobj.value == None
    assert maxobj.value == None
    assert maxobj.index == None
    assert minobj.index == None



def gen_arrays(start=10,stop=350,step=8):
    for x in range(start,stop,step):
        yield [randint(-300,300) for i in range(x)]
