#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Testing operation and coverage for context module in tests directory."""

import os

import pytest

from tests.context import Con, mkfolder, rmpath, teardown, testfile


def test_seq():
    """Test seq function for random string output."""
    output = Con.seq
    assert isinstance(output, str)   # nosec
