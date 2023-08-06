# Python package to communicate with ub

Python package to communicate with ublox chipsets

To install the package:

```bash
pip3 install pyublox
```

## Testing the package

This package uses the pytest suite, to execute the tests, issue the following
command

```bash
pytest -v /path/to/source
```

### Development within a Docker container

The best way to develop the package is by using a controlled environement.
To do this, run a Python 3.7 container like so

```bash
docker run -v `pwd`:/pyublox -ti rokubun/gcc:debian-python3.7 bash
```

Once within the container type the following commands:

```bash
# The package requires git to work properly
cd /pyublox
pip install -e .
```

## Submission to PyPi

In order to deploy to PyPi

```bash
# Update setuptools
python3 -m pip install --user --upgrade setuptools wheel

# Create the distribution wheel
python3 setup.py sdist bdist_wheel

# Upload the distribution wheels to the PyPi repo
python3 -m twine upload dist/*
```

More details on deployment can be found [here](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives).
