from setuptools import find_packages, setup


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pyublox',
    version_cc='{version}',
    author='Rokubun',
    author_email='info@rokubun.cat',
    description='Interface with ublox chipsets using Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='http://opensource.org/licenses/MIT',
    url="https://github.com/rokubun/pyublox",
    setup_requires=['setuptools-git-version-cc'],
    packages=["pyublox"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "docopt",
        "twine",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'pyublox = pyublox.main:main'
        ]
    }
)

