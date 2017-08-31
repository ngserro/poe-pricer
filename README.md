# poe-pricer

## Description

poe-pricer is a script to help you price your Unique items in [Path of Exile](https://www.pathofexile.com/). It outputs a well formated table for each stash tab you have, with a line with each Unique you have and a sugested price, based on information from [poe.ninja](http://poe.ninja/). It also shows your top 10 most valuable items and a total sum of all item values.

## Installation

### Requirements

* An internet connection
* Python

Python modules required:

* requests
* argparse
* termcolor
* tabulate

`poe-pricer.py` was tested in Windows, Linux (Ubuntu) and macOS. The tested version of python was 2.7.12.

Before you download anything you should make sure that you have python and the required modules installed.
Example for debian like OS:

```bash
sudo apt-get update;
sudo apt-get install python python-pip;
pip install requests argparse termcolor tabulate
```
In Windows:

Install python from [www.python.org](https://www.python.org/downloads/release/python-2713/), then install the modules with pip:

```cmd
C:\Python27\Scripts\pip.exe install requests argparse argparse argparse
```

### Using Git

The repository can be cloned to any location.

```bash
git clone https://github.com/ngserro/poe-pricer.git
```

### Git-free installation

To install without Git:

```bash
cd; curl -#L https://github.com/ngserro/poe-pricer/tarball/master | tar -xzv 
```

If you want to update you can simply run that command again.

## Usage

```bash
usage: pricer.py [-h] POESESSID account league

positional arguments:
  POESESSID   Use your POESESSID
  account     Your POE account name
  league      POE league

optional arguments:
  -h, --help  show this help message and exit
```

Example:

```bash
python poe-pricer.py d2aytrgsd123z16aet9mgjasfj775jgda GGGChrisAccount Standard
```

## Thanks to…

* [Grinding Gear Games](https://www.pathofexile.com/) for making Path of Exile
* [poe.ninja](http://poe.ninja/) for all the item price information