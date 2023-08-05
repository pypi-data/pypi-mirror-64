import io
import os

from setuptools import find_packages, setup

NAME = 'vectorslow'
DESCRIPTION = 'Think tensorflow but in python and poorly written'
URL = 'https://github.com/bigthonk/vectorslow'
EMAIL = 'CarrollD@aetna.com'
AUTHOR = 'Dan Carroll'
VERSION = 1.1

# What packages are required for this module to be executed?
REQUIRED = [
    'numpy'
]

here = os.path.abspath(os.path.dirname(__file__))[:-3]

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True
)

