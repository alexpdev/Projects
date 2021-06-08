#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# MinMaxObj  extends builtin min and max functions.
# Copyright (C) 2021 alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import random
from time import time

import pytest

from MinMax import (EmptySequenceError, InputError, Max, Min, MinMax, max_get, min_get,
                    minmax_get)


def timer(func):
    """Decorate functions to calculate the time taken to run and return."""

    def wrapper(*args, **kwargs):
        print(func.__name__)
        then = time()
        result = func(*args, **kwargs)
        now = time()

        print(f"completed in {now - then} seconds")
        return result

    return wrapper


def array_gen():
    for size in range(100, 20000, 100):
        seq = []
        while size > 0:
            sm, lg = random.randint(-1000, 0), random.randint(0, 7000)
            elem = random.randint(sm, lg)
            seq.append(elem)
            size -= 1
        yield seq


@timer
def test_min_speed():
    mins = []
    for arr in array_gen():
        m = min(arr)
        i = arr.index(m)
        assert arr[i] == m
        mins.append([m, i])
    return True


@timer
def test_min_get_speed():
    mins = []
    for arr in array_gen():
        m, i = struc = min_get(arr)
        assert arr[i] == m
        mins.append(struc)
    return True


class TestMinMaxFunctions:
    @timer
    def test_max_get(self):
        for seq in [[], ""]:
            assert pytest.raises(EmptySequenceError, max_get, seq)
        for var in [None, 7, True, False, 0]:
            assert pytest.raises(InputError, max_get, var)
        for seq in array_gen():
            max_val, max_ind = max_get(seq)
            assert max_val == max(seq)
            assert seq[max_ind] == max_val
        for seq in [[3], (3,)]:
            max_val, max_ind = max_get(seq)
            assert max_val == max(seq)
            assert max_val == 3
            assert seq[max_ind] == max_val
            assert seq[max_ind] == 3
            assert max_ind == 0
        return True

    @timer
    def test_min_get(self):
        for seq in [{}, [], set()]:
            assert pytest.raises(EmptySequenceError, min_get, seq)
        for var in [None, 7, True, False, 0]:
            assert pytest.raises(InputError, min_get, var)
        for seq in array_gen():
            min_val, min_ind = min_get(seq)
            assert min_val == min(seq)
            assert seq[min_ind] == min_val
        for seq in [[3], (3,)]:
            min_val, min_ind = min_get(seq)
            assert min_val == min(seq)
            assert min_val == 3
            assert seq[min_ind] == min_val
            assert seq[min_ind] == 3
            assert min_ind == 0
        return True

    @timer
    def test_minmax_get(self):
        for seq in [{}, [], set()]:
            assert pytest.raises(EmptySequenceError, minmax_get, seq)
        for var in [None, 7, True, False, 0]:
            assert pytest.raises(InputError, minmax_get, var)
        for seq in array_gen():
            (minval, minind), (maxval, maxind) = minmax_get(seq)
            assert maxval == max(seq)
            assert minval == min(seq)
            assert seq[maxind] == maxval
            assert seq[minind] == minval
        for seq in [[3], (3,)]:
            (minval, minind), (maxval, maxind) = minmax_get(seq)
            assert maxval == max(seq)
            assert maxval == 3
            assert minval == min(seq)
            assert minval == 3
            assert seq[maxind] == maxval
            assert seq[maxind] == 3
            assert seq[minind] == minval
            assert seq[minind] == 3
        return True


class TestMinMaxClasses:
    @timer
    def test_Min(self):
        for seq in [{}, [], set()]:
            assert pytest.raises(EmptySequenceError, Min, seq)
        for var in [None, 7, True, False, 0]:
            assert pytest.raises(InputError, Min, var)
        for seq in array_gen():
            min_ = Min(seq)
            assert min_.value == min(seq)
            assert seq[min_.index] == min_.value
        for seq in [[3], (3,)]:
            min_ = Min(seq)
            assert min_.value == min(seq)
            assert min_.value == 3
            assert seq[min_.index] == min_.value
            assert seq[min_.index] == 3
            assert min_.index == 0
        return True

    @timer
    def test_Max(self):
        for seq in [{}, [], set()]:
            assert pytest.raises(EmptySequenceError, Max, seq)
        for var in [None, 7, True, False, 0]:
            assert pytest.raises(InputError, Max, var)
        for seq in array_gen():
            max_ = Max(seq)
            assert max_.value == max(seq)
            assert seq[max_.index] == max_.value
        for seq in [[3], (3,)]:
            max_ = Max(seq)
            assert max_.value == max(seq)
            assert max_.value == 3
            assert seq[max_.index] == max_.value
            assert seq[max_.index] == 3
            assert max_.index == 0
        return True

    @timer
    def test_MinMax(self):
        for seq in [{}, [], set()]:
            assert pytest.raises(EmptySequenceError, MinMax, seq)
        for var in [None, 7, True, False, 0]:
            assert pytest.raises(InputError, MinMax, var)
        for seq in array_gen():
            minmax = MinMax(seq)
            assert minmax.min_value == min(seq)
            assert seq[minmax.min_index] == minmax.min_value
            assert minmax.max_value == max(seq)
            assert seq[minmax.max_index] == minmax.max_value
        for seq in [[3], (3,)]:
            minmax = MinMax(seq)
            assert minmax.min_value == min(seq)
            assert minmax.min_value == 3
            assert seq[minmax.min_index] == minmax.min_value
            assert seq[minmax.min_index] == 3
            assert minmax.max_value == max(seq)
            assert minmax.max_value == 3
            assert seq[minmax.max_index] == minmax.max_value
            assert seq[minmax.max_index] == 3
            assert minmax.max_index == 0
            assert minmax.min_index == 0
        return True


def conf(func):
    assert func() == True


if __name__ == "__main__":
    classes = TestMinMaxClasses()
    funcs = TestMinMaxFunctions()
    tests = [
        funcs.test_max_get,
        funcs.test_min_get,
        funcs.test_minmax_get,
        classes.test_Max,
        classes.test_Min,
        classes.test_MinMax,
        test_min_speed,
        test_min_get_speed,
    ]
    map(lambda x: conf(x), tests)
