# MinMaxObj

![Python](https://img.shields.io/badge/python-3.3%2B-green)
![License](https://img.shields.io/badge/GNU%20LGPL-blue)

MinMaxObj is a utility library containing classes and functions that extend python's built in `min()` and `max()` functions.

## Requires

- Python 3+
- pip

## Installing

```Windows:
pip install MinMaxObj-alexpdev
```

## Usage

Import the module into your source code as needed.

```python:
import MinMaxObj
from MinMaxObj import get_min, Max, MinMax
```

## Classes

- Min
  - requires an iterable sequence to construct
  - stores the minimum value
  - stores the minimum value index
- Max
  - requires an iterable sequence to construct
  - stores the maximum value
  - stores the maximum value index
- MinMax
  - requires an iterable sequence to construct
  - stores the minimum and maximum values
  - stores the minimum and maximum value indeces

## Functions

- min_get
  - requires and iterable sequence as arguement
  - calculates and returns minimum value and it's index
- max_get
  - requires and iterable sequence as arguement
  - calculates and returns maximum value and it's index
- minmax_get
  - requires and iterable sequence as arguement
  - calculates and returns minimum and maximum values and their indeces

## License

GNU Lesser General Public License v3.0
