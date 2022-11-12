<<<<<<< HEAD
<<<<<<< HEAD
# Simple-Fun-Tools-and-Games

* These are games and projects I am doing in my leisure time.
# minmaxplus

!["MinMax+"](./assets/minmaxplus.png)

Small library that extends python's built in `min` and `max` functions.

## Installing

`pip install minmaxplus`

## Usage

Import the module into your source code as needed.

```python
import minmaxplus
from minmaxplus import minp, maxp, minmaxp
```

## Functions

- minp

  - requires indexed iterable sequence as arguement
  - calculates and returns minimum value and it's index

- maxp

  - requires indexed iterable sequence as arguement
  - calculates and returns maximum value and it's index

- minmax

  - requires an indexed iterable sequence as arguement
  - calculates and returns minimum and maximum values and their indeces

## License

GNU Lesser General Public License v3.0
# Bitprint

A tiny CLI for converting integers to binary.

## Dependencies

- Python 3.*

## Installation

```powershell
git clone https://github.com/alexpdev/bitprint.git
cd bitprint
python setup.py install
=======
# ElectronTorrentfile

![torrentfileJS](https://github.com/alexpdev/torrentfilejs/blob/master/public/torrentfilejs.png)

----

![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/electrontorrentfile?color=purple&logo=electron&logoColor=orange&style=plastic)
![GitHub](https://img.shields.io/github/license/alexpdev/electrontorrentfile?color=maroon&logo=apache&logoColor=skyblue&style=plastic)
![GitHub package.json dependency version (dev dep on branch)](https://img.shields.io/github/package-json/dependency-version/alexpdev/electrontorrentfile/dev/electron?logo=electron&logoColor=orangered&style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/alexpdev/electrontorrentfile?color=skyblue&logo=github&logoColor=orange&style=plastic)

A Desktop GUI form for creating Bittorrent Meta Files of any content in your local filesystem.  

TorrentfileJS allows fine-grain controls over your bittorrent files size and 
contents, it allows for including comments and cross-seed source inputs. 
TorrentfileJs supports all versions of meta-files and provides the same 
level of cutomization for each, including hybrids. 

## Requirements

- nodejs
- electronjs
- vue 3
- bootstrap
- typescript

## Installation

```bash
git clone https://github.com/alexpdev/electrontorrentfile.git
cd electrontorrentfile
npm install .
# or
yarn add .
>>>>>>> 28e86b5a6d04e848413a728d58194aec7e587120
```

## Usage

<<<<<<< HEAD
```powershell
> bitprint 1
1
> bitprint 2
10
> bitprint 12
1100
=======
```bash
npm run electron:build
npm run start
npm run electron:dev
npm run production
>>>>>>> 28e86b5a6d04e848413a728d58194aec7e587120
```

## License

<<<<<<< HEAD
[MIT](https://github.com/alexpdev/bitprint/_todo_)
# TorrentFile

![torrentfile](https://github.com/alexpdev/torrentfile/blob/master/assets/torrentfile.png?raw=true)

------

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/202440df15224535b5358503e6235c88)](https://www.codacy.com/gh/alexpdev/TorrentFile/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alexpdev/TorrentFile&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/alexpdev/TorrentFile/branch/master/graph/badge.svg?token=PXFsxXVAHW)](https://codecov.io/gh/alexpdev/TorrentFile)
![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/TorrentFile)
![GitHub License](https://img.shields.io/github/license/alexpdev/TorrentFile)
![PyPI - Downloads](https://img.shields.io/pypi/dw/torrentfile)
[![CI](https://github.com/alexpdev/TorrentFile/actions/workflows/python_workflow.yml/badge.svg?branch=master&event=push)](https://github.com/alexpdev/TorrentFile/actions/workflows/python_workflow.yml)
[![DeepSource](https://deepsource.io/gh/alexpdev/TorrentFile.svg/?label=active+issues&token=16Sl_dF7nTU8YgPilcqhvHm8)](https://deepsource.io/gh/alexpdev/TorrentFile/)

## :globe_with_meridians: Overview

A `simple` and `convenient` tool for creating, reviewing, editing, and/or  
checking/validating bittorrent meta files (aka torrent files). _`torrentfile`_  
supports all versions of Bittorrent files, including hybrid meta files.

> A GUI frontend for this project can be found at [https://github.com/alexpdev/TorrentfileQt](https://github.com/alexpdev/TorrentfileQt)

## :white_check_mark: Requirements

- Python 3.7+
- Tested on Linux and Windows

## :package: Install

__via PyPi:__

    pip install torrentfile

__via Git:__

    git clone https://github.com/alexpdev/torrentfile.git
    python setup.py install

> Download pre-compiled binaries from the [release page](https://github.com/alexpdev/torrentfile/releases).

## :scroll: Documentation

Documentation can be found  [here](https://alexpdev.github.io/TorrentFile)
or in the _`docs`_ directory.

## :rocket: Usage

```bash
torrentfile [-h] [-i] [-V] [-v]  ...

Sub-Commands:

    create           Create a new torrent file.
    check            Check if file/folder contents match a torrent file.
    edit             Edit a pre-existing torrent file.

optional arguments:
  -h, --help         show this help message and exit
  -V, --version      show program version and exit
  -i, --interactive  select program options interactively
  -v, --verbose      output debug information
```

> Usage examples can be found in the project documentation on the [examples page.](https://alexpdev.github.io/TorrentFile/examples)

## :memo: License

Distributed under the GNU LGPL v3. See `LICENSE` for more information.

## :bug: Issues

If you encounter any bugs or would like to request a new feature please open a new issue.

[https://github.com/alexpdev/TorrentFile/issues](https://github.com/alexpdev/TorrentFile/issues)
# FTP

Will fill in later.

TODO:
add logging
finish client commands
=======
# osslicensor
>>>>>>> 79e38535999f90130c25c5c4501401fa1de2bd09
=======
ElectronTorrentfile is liscensed under the Apache 2.0 Open Source Software License
see the LICENSE file in the root directory for more details.

## Related Projects

- [torrentfile](https://githube.com/alexpdev/torrentfile)  A CLI multitool for all things torrent files
- [torrentfileQt](https://github.com/alexpdev/torrentfileQt) A much more robust and tested torrent file GUI tool
- [pybem](https://github.com/alexpdev/pyben) The Bencode library used in torrentfile and TorrentfileQt

All of these projects are written with python and have a much more robust featureset and have much better test
coverage.

## Contributing

All PR's or feature requests are  Welcome.
>>>>>>> 28e86b5a6d04e848413a728d58194aec7e587120
