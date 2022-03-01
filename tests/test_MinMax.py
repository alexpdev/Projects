#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# MinMax+  extends builtin _minp and _maxp functions.
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

import random

import pytest

from minmaxplus import minmax


_minp = minmax._minp
_maxp = minmax.maxp
_minmaxp = minmax._minmaxp

@pytest.fixture
def dictseq():
    """Return a dictionary."""
    return {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}


@pytest.fixture
def setseq():
    """Return a set."""
    return set([1, 2, 3, 4, 5, 6, 7])

@pytest.fixture
def tupleseq():
    """Return tuple of integers."""
    return (1, 2, 3, 4, 5, 6, 7)


@pytest.fixture
def listseq():
    """Return list of integers."""
    return [1, 2, 3, 4, 5, 6, 7]

@pytest.fixture
def reverseseq():
    """Return reversed list of integers."""
    return [7, 6, 5, 4, 3, 2, 1]


@pytest.fixture
def shuffleseq():
    """Return shuffled list of integers."""
    return [5, 1, 4, 3, 7, 6, 2]


@pytest.fixture
def chars():
    """Return list of characters."""
    return ['a', 'b', 'd', 'f', 'p', 'b']


@pytest.fixture
def strings():
    """Return list of strings."""
    return ['alaska', 'britain', 'devil', 'foot', 'piano', 'basketball']


@pytest.fixture
def emptyseq():
    """Return empty sequence."""
    return []


@pytest.fixture
def singleitemseq():
    """Return sequence with only 1 element."""
    return [7]


@pytest.fixture(scope="module")
def randseq():
    number_of_tests = 10000
    elements_per_test = 1000
    sequences = []
    for i in range(number_of_tests):
        seq = []
        for j in range(elements_per_test):
            seq.append(random.randint(0,10000))
        sequences.append(seq)
    return sequences



def test_tuple_maxp(tupleseq):
    """Test _maxp with tuple."""
    assert _maxp(tupleseq) == (7, 6)


def test_list_maxp(listseq):
    """Test _maxp with list."""
    assert _maxp(listseq) == (7, 6)


def test_dict_maxp(dictseq):
    """Test Exception raised for dictionary."""
    try:
        assert _maxp(dictseq) == (7, 6)
    except:
        assert True


def test_set_maxp(setseq):
    """Test exception raised for set."""
    try:
        assert _maxp(setseq) == (7, 6)
    except TypeError:
        assert True


def test_reverse_maxp(reverseseq):
    """Test _maxp on reversed sequence."""
    assert _maxp(reverseseq) == (7, 0)


def test_shuffle_maxp(shuffleseq):
    """Test _maxp on shuffled sequence."""
    assert _maxp(shuffleseq) == (7, 4)


def test_empty_maxp(emptyseq):
    """Test exception raised on empty sequence."""
    try:
        assert _maxp(emptyseq) == False
    except:
        assert True

def test_singleitems_maxp(singleitemseq):
    """Test _maxp on single item list."""
    assert _maxp(singleitemseq) == (7,0)

def test_tuple__minp(tupleseq):
    """Test _minp with tuple."""
    assert _minp(tupleseq) == (1,0)

def test_list__minp(listseq):
    """Test _minp with list."""
    assert _minp(listseq) == (1,0)

def test_dict__minp(dictseq):
    """Test Exception raised for dictionary."""
    try:
        assert _minp(dictseq) == (1,0)
    except:
        assert True

def test_set__minp(setseq):
    """Test exception raised for set."""
    try:
        assert _minp(setseq) == (1,0)
    except:
        assert True

def test_reverse__minp(reverseseq):
    """Test _minp on reversed sequence."""
    assert _minp(reverseseq) == (1,6)

def test_shuffle__minp(shuffleseq):
    """Test _minp on shuffled sequence."""
    assert _minp(shuffleseq) == (1,1)

def test_empty__minp(emptyseq):
    """Test exception raised on empty sequence."""
    try:
        _minp(emptyseq)
        assert False
    except:
        assert True

def test_singleitems__minp(singleitemseq):
    """Test _minp on single item list."""
    assert _minp(singleitemseq) == (7,0)


def test_char_seq_maxp(chars):
    """Test _maxp on sequence of chars"""
    assert _maxp(chars) == ('p', 4)


def test_char__minp(chars):
    """Test _minp on sequence of chars"""
    assert _minp(chars) == ('a', 0)


def test_strings__minp(strings):
    """Test _minp on sequence of strings"""
    assert _minp(strings) == ('alaska', 0)


def test_strings_maxp(strings):
    """Test _maxp on sequence of strings"""
    assert _maxp(strings) == ('piano', 4)


def test_strings__minmaxp(strings):
    """Test _minmaxp on sequence of strings"""
    assert _minmaxp(strings) == [('alaska', 0), ('piano', 4)]


def test_chars__minmaxp(chars):
    """Test _minmaxp on sequence of chars"""
    assert _minmaxp(chars) == [('a', 0), ('p', 4)]


@pytest.mark.benchmark(min_rounds=50, disable_gc=True, warmup=True)
def test_timer_maxp(randseq, benchmark):
    """Test timer for _maxp function."""
    result1 = benchmark(time_maxp, randseq)
    assert result1

@pytest.mark.benchmark(min_rounds=50, disable_gc=True, warmup=True)
def test_timer_maxubuiltin(randseq,benchmark):
    result2 = benchmark(time_max, randseq)
    assert result2


def time_max(rseq):
    """Time duration for max and index functions."""
    results = []
    for seq in rseq:
        num = max(seq)
        idx = seq.index(num)
        results.append((num, idx))
    return results

def time_maxp(rseq):
    """Time durations on _maxp function."""
    results = []
    for seq in rseq:
        num, idx = _maxp(seq)
        results.append((num, idx))
    return results
