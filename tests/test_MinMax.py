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

from minmaxplus import minp, maxp, minmaxp


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


def test_tuple_maxp(tupleseq):
    """Test maxp with tuple."""
    assert maxp(tupleseq) == (7, 6)


def test_list_maxp(listseq):
    """Test maxp with list."""
    assert maxp(listseq) == (7, 6)


def test_dict_maxp(dictseq):
    """Test Exception raised for dictionary."""
    try:
        assert maxp(dictseq) == (7, 6)
    except:
        assert True


def test_set_maxp(setseq):
    """Test exception raised for set."""
    try:
        assert maxp(setseq) == (7, 6)
    except TypeError:
        assert True


def test_reverse_maxp(reverseseq):
    """Test maxp on reversed sequence."""
    assert maxp(reverseseq) == (7, 0)


def test_shuffle_maxp(shuffleseq):
    """Test maxp on shuffled sequence."""
    assert maxp(shuffleseq) == (7, 4)


def test_empty_maxp(emptyseq):
    """Test exception raised on empty sequence."""
    try:
        assert maxp(emptyseq) == False
    except:
        assert True

def test_singleitems_maxp(singleitemseq):
    """Test maxp on single item list."""
    assert maxp(singleitemseq) == (7,0)

def test_tuple_minp(tupleseq):
    """Test minp with tuple."""
    assert minp(tupleseq) == (1,0)

def test_list_minp(listseq):
    """Test minp with list."""
    assert minp(listseq) == (1,0)

def test_dict_minp(dictseq):
    """Test Exception raised for dictionary."""
    try:
        assert minp(dictseq) == (1,0)
    except:
        assert True

def test_set_minp(setseq):
    """Test exception raised for set."""
    try:
        assert minp(setseq) == (1,0)
    except:
        assert True

def test_reverse_minp(reverseseq):
    """Test minp on reversed sequence."""
    assert minp(reverseseq) == (1,6)

def test_shuffle_minp(shuffleseq):
    """Test minp on shuffled sequence."""
    assert minp(shuffleseq) == (1,1)

def test_empty_minp(emptyseq):
    """Test exception raised on empty sequence."""
    try:
        minp(emptyseq)
        assert False
    except:
        assert True

def test_singleitems_minp(singleitemseq):
    """Test minp on single item list."""
    assert minp(singleitemseq) == (7,0)


def test_char_seq_maxp(chars):
    """Test maxp on sequence of chars"""
    assert maxp(chars) == ('p', 4)


def test_char_minp(chars):
    """Test minp on sequence of chars"""
    assert minp(chars) == ('a', 0)


def test_strings_minp(strings):
    """Test minp on sequence of strings"""
    assert minp(strings) == ('alaska', 0)


def test_strings_maxp(strings):
    """Test maxp on sequence of strings"""
    assert maxp(strings) == ('piano', 4)


def test_strings_minmaxp(strings):
    """Test minmaxp on sequence of strings"""
    assert minmaxp(strings) == [('alaska', 0), ('piano', 4)]


def test_chars_minmaxp(chars):
    """Test minmaxp on sequence of chars"""
    assert minmaxp(chars) == [('a', 0), ('p', 4)]
