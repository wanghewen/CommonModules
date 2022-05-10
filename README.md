# CommonModules

This package is meant to provide some shortcuts for **Python** programmers when solving problems.  

## Prerequisite

**[Anaconda](https://www.continuum.io/downloads/)** (A Python distribution with many useful packages) is recommended before using this package.

*If this is not installed, some errors may happen during package installation, most likely related to scipy and numpy.*

## Installation
You can also use `pip install CommonModules` to install this package.

## Usage

 `import CommonModules as CM`

Example: list all files under current working directory

 `CM.IO.ListFiles(".", ".")`

Please refer to **[http://commonmodules.readthedocs.io/en/latest/](http://commonmodules.readthedocs.io/en/latest/)** for more information.  

Wecome any issues or pull requests~


## Development
### Upload to PyPI:
Install `twine` through `pip install twine`

`rm -rf ./dist`

`python setup.py sdist bdist_wheel`

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

`twine upload dist/*`
