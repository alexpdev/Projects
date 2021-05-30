#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Objects and functions that provide a more robust way to deal with minimum and maximum values in an array or sequence.
"""

import sys

class InputError(Exception):
    pass

class EmptySequenceError(Exception):
    pass

class Min:
    """Searches and stores the value and index of minimum element in sequence.
    """

    def __init__(self,seq):
        """__init__ Constructor for Min class.

        Args:
            value (any, optional): Minimum value to store. Defaults to None.
            index (int, optional): Index of minimum value in sequence. Defaults to None.
        """
        if not hasattr(seq,'__len__'):
            raise InputError
        if len(seq) == 0:
            raise EmptySequenceError
        self.value = None
        self.index = None
        self.seq = seq
        self.findmin()

    @classmethod
    def get(cls,seq):
        """Construct a Min instance from arguement and returns minimum value and index.

        Args:
            seq (list, dict, set, ...): any iterable.

        Raises:
            TypeError: when arguement isn't iterable.
            EmptySequenceError: when arguement is empty.

        Returns:
            (any, int): Tuple containing minimum value and it's index of the provided sequence.
        """
        least = cls(seq)
        return (least.value, least.index)

    def __len__(self):
        """Return the length of input sequence."""
        return len(self.seq)

    def __str__(self):
        """Generates a string containing the value and index currently stored."""
        return f"value={self.value}, index={self.index}"

    def __repr__(self):
        """Generates string representation of Min Object instance."""
        return f"(Min| value:{self.value}, index:{self.index})"

    def findmin(self):
        """findMin search sequence provided for it's minumum value.

        This method stores the minimum value and it's index in it's value and index attributes.
        Method is part of constructor and does not return.
        """
        min_, min_i, n = sys.maxsize, 0, len(self.seq)
        if n & 1: n -= 1
        for index in range(0, n, 2):
            if self.seq[index + 1] < self.seq[index]:
                minimum, index = self.seq[index + 1], index + 1
            else:
                minimum, index = self.seq[index], index
            if minimum < min_:
                min_, min_i = minimum, index
        if len(self.seq) & 1:
            if self.seq[n] < min_:
                min_, min_i = self.seq[n], n
        self.index = min_i
        self.value = min_


class Max:
    """Searches and stores the value and index of maximum element in a sequence.
    """

    def __init__(self,seq):
        """__init__ Constructor for Max class.

        Args:
            value (any, optional): Maximum value to store. Defaults to None.
            index (int, optional): Index of maximum value in sequence. Defaults to None.
        """
        if not hasattr(seq,'__len__'):
            raise InputError
        if len(seq) == 0:
            raise EmptySequenceError
        self.value = None
        self.index = None
        self.seq = seq
        self.findmax()

    @classmethod
    def get(cls,seq):
        """Construct a Max instance from arguement and returns maximum value and index.

        Args:
            seq (list, dict, set, ...): any iterable.

        Raises:
            TypeError: when arguement isn't iterable.
            EmptySequenceError: when arguement is empty.

        Returns:
            (any, int): Tuple containing maximum value and it's index of the provided sequence.
        """
        maximum = cls(seq)
        return (maximum.value, maximum.index)

    def __repr__(self):
        """Generates string representation of Max Object instance."""
        return f"(Max| value:{self.value}, index:{self.index})"

    def __len__(self):
        """Return the length of input sequence."""
        return len(self.seq)

    def __str__(self):
        """Generates a string containing the value and index currently stored."""
        return f"value={self.value}, index={self.index}"

    def findmax(self):
        """findmax search sequence provided for it's maximum value.

        This method stores the maximum value and it's index in it's value and index attributes.
        Method is part of constructor and does not return.
        """
        max_, max_i, n = -sys.maxsize, 0, len(self.seq)
        # check if length is odd
        if n & 1: n -= 1
        # compare elements to maximum variable
        for i in range(0,n,2):
            if self.seq[i+1] > self.seq[i]:
                maximum, index = self.seq[i+1], i+1
            else:
                maximum, index = self.seq[i], i
            if maximum > max_:
                max_, max_i = maximum, index
        # if length was odd then compare with last element
        if len(self.seq) & 1:
            if self.seq[n] > max_:
                max_, max_i = self.seq[n], n
        self.index = max_i
        self.value = max_


class MinMax:
    """Searches and stores the value and index of maximum element in a sequence.
    """

    def __init__(self,seq):
        """__init__ Constructor for Max class.

        Args:
            value (any, optional): Maximum value to store. Defaults to None.
            index (int, optional): Index of maximum value in sequence. Defaults to None.
        """
        if not hasattr(seq,'__len__'):
            raise InputError
        if len(seq) == 0:
            raise EmptySequenceError
        self.min_value = None
        self.min_index = None
        self.max_value = None
        self.max_index = None
        self.seq = seq
        self.findminmax()

    @classmethod
    def get(cls,seq):
        """Construct a Max instance from arguement and returns maximum value and index.

        Args:
            seq (list, dict, set, ...): any iterable.

        Raises:
            TypeError: when arguement isn't iterable.
            EmptySequenceError: when arguement is empty.

        Returns:
            (any, int): Tuple containing maximum and minimum value and it's index of the provided sequence.
        """
        minmax = cls(seq)
        return ((minmax.min_value, minmax.min_index), (minmax.max_value, minmax.max_index))

    def __repr__(self):
        """Generates string representation of Max Object instance."""
        return str(self)

    def __str__(self):
        """Generates a string containing the value and index currently stored."""
        return f"({self.min_value}, {self.min_index}), ({self.max_value}, {self.max_index})"

    def findminmax(self):
        """findminmax search sequence provided for it's maximum and minimum value.

        This method stores the maximum and minimum value and it's index
        in it's value and index attributes. Method is part of constructor and does not return.
        """
        max_, max_i, n = -sys.maxsize, 0, len(self.seq)
        min_, min_i = sys.maxsize, 0
        # checks if seq length is odd
        if n & 1: n -= 1
        for i in range(0,n,2):
            if self.seq[i+1] > self.seq[i]:
                maximum, maxindex = self.seq[i+1], i + 1
                minimum, minindex = self.seq[i], i
            else:
                minimum, minindex = self.seq[i+1], i + 1
                maximum, maxindex = self.seq[i], i
            if maximum > max_: max_, max_i = maximum, maxindex
            if minimum < min_: min_, min_i = minimum, minindex
        # checks if seq length is odd
        if len(self.seq) & 1:
            if self.seq[n] > max_: max_, max_i = self.seq[n], n
            if self.seq[n] < min_: min_, min_i = self.seq[n], n
        self.min_value = min_
        self.max_value = max_
        self.min_index = min_i
        self.max_index = max_i


def max_get(seq):
    """Get array element and index with maximum value.

    - Args:
        seq list/dict/tuple/set: any iterable sequence

    - Returns:
        (sny,int) : (max_value, max_index)
    """

    if not hasattr(seq,'__len__'):
        raise InputError
    if len(seq) == 0:
        raise EmptySequenceError
    max_, max_i, n = -sys.maxsize, 0, len(seq)
    # checks if seq length is odd
    if n & 1: n -= 1
    for i in range(0,n,2):
        if seq[i+1] > seq[i]: maximum, index = seq[i+1], i+1
        else: maximum, index = seq[i], i
        if maximum > max_: max_, max_i = maximum, index
    # checks if seq length is odd
    if len(seq) & 1:
        if seq[n] > max_: max_, max_i = seq[n], n
    return (max_,max_i)


def min_get(seq):
    """Get array element and index with maximum value.

    Args:
        list/dict/tuple/set: any iterable sequence.

    - Returns:
        (any,int) (min_value, min_index)
    """

    if not hasattr(seq,'__len__'):
        raise InputError
    if len(seq) == 0:
        raise EmptySequenceError
    min_, min_i, n = sys.maxsize, 0, len(seq)
    # checks if seq length is odd
    if n & 1: n -= 1
    for i in range(0,n,2):
        if seq[i+1] < seq[i]: minimum, index = seq[i+1], i+1
        else: minimum, index = seq[i], i
        if minimum < min_: min_, min_i = minimum, index
    # checks if seq length is odd
    if len(seq) & 1:
        if seq[n] < min_: min_, min_i = seq[n], n
    return (min_, min_i)


def minmax_get(seq):
    """Get value and index of maximum element and minimum elements in array.

    Args:
        arr ([list/tuple/set/dict]): Any iterable

    - Returns:
        (any,int),(any,int): [(max_value,max_index),(min_value,min_index)]
    """
    if not hasattr(seq,'__len__'):
        raise InputError
    if len(seq) == 0:
        raise EmptySequenceError
    max_, max_i, n = -sys.maxsize, 0, len(seq)
    min_, min_i = sys.maxsize, 0
    # checks if seq length is odd
    if n & 1: n -= 1
    for i in range(0,n,2):
        if seq[i+1] > seq[i]:
            maximum, maxindex = seq[i+1], i + 1
            minimum, minindex = seq[i], i
        else:
            minimum, minindex = seq[i+1], i + 1
            maximum, maxindex = seq[i], i
        if maximum > max_: max_, max_i = maximum, maxindex
        if minimum < min_: min_, min_i = minimum, minindex
    # checks if seq length is odd
    if len(seq) & 1:
        if seq[n] > max_: max_, max_i = seq[n], n
        if seq[n] < min_: min_, min_i = seq[n], n
    return [(min_,min_i),(max_,max_i)]
