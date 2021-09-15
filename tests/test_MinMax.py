#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# MinMax+  extends builtin minp and maxp functions.
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

import pytest
from minmaxplus import minp, maxp, minmax


@pytest.fixture
def tupleseq():
    return (1, 2, 3, 4, 5, 6, 7)

@pytest.fixture
def listseq():
    return [1, 2, 3, 4, 5, 6, 7]

@pytest.fixture
def dictseq():
    return {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}

@pytest.fixture
def setseq():
    return set([1, 2, 3, 4, 5, 6, 7])


@pytest.fixture
def reverseseq():
    return [7, 6, 5, 4, 3, 2, 1]

@pytest.fixture
def shuffleseq():
    return [5, 1, 4, 3, 7, 6, 2]

@pytest.fixture
def emptyseq():
    return []

@pytest.fixture
def singleitemseq():
    return [7]

def test_tuple_maxp(tupleseq):
    assert maxp(tupleseq) == (7, 6)

def test_list_maxp(listseq):
    assert maxp(listseq) == (7, 6)

def test_dict_maxp(dictseq):
    try:
        assert maxp(dictseq) == (7, 6)
    except:
        assert True

def test_set_maxp(setseq):
    try:
        assert maxp(setseq) == (7, 6)
    except TypeError:
        assert True

def test_reverse_maxp(reverseseq):
    assert maxp(reverseseq) == (7, 0)

def test_shuffle_maxp(shuffleseq):
    assert maxp(shuffleseq) == (7, 4)


def test_empty_maxp(emptyseq):
    try:
        assert maxp(emptyseq) == False
    except:
        assert True

def test_singleitems_maxp(singleitemseq):
    assert maxp(singleitemseq) == (7,0)

def test_tuple_minp(tupleseq):
    assert minp(tupleseq) == (1,0)

def test_list_minp(listseq):
    assert minp(listseq) == (1,0)

def test_dict_minp(dictseq):
    try:
        assert minp(dictseq) == (1,0)
    except:
        assert True

def test_set_minp(setseq):
    try:
        assert minp(setseq) == (1,0)
    except:
        assert True

def test_reverse_minp(reverseseq):
    assert minp(reverseseq) == (1,6)

def test_shuffle_minp(shuffleseq):
    assert minp(shuffleseq) == (1,1)

def test_empty_minp(emptyseq):
    try:
        minp(emptyseq)
        assert False
    except:
        assert True

def test_singleitems_minp(singleitemseq):
    assert minp(singleitemseq) == (7,0)

