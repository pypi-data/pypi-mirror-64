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
