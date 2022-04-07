import sys
import argparse

def execute(args=None):
    if not args:
        args = sys.argv
    parser = argparse.ArgumentParser("bitprint")
    parser.add_argument("-v", help="verbose", action="store_true")
    parser.add_argument("value", action="store")
    names = parser.parse_args(args[1:])
    print(bin(int(names.value))[2:])
