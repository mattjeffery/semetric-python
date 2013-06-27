import os
import datetime
from setuptools import setup, find_packages

# Utility function to read the README file, etc..
def read(fname):
    fh = None
    try:
        fh = open(os.path.join(os.path.dirname(__file__), fname))
    except:
        if fh:
            fh.close()
        raise
    return fh.read()

setup(
    name="semetric.apiclient",
    version="0.0.1",
    author="Matt Jeffery",
    author_email="matt@clan.se",
    # read the install requirements from the requirements.txt
    install_requires=read("requirements.txt").splitlines(),
    description=("Wrapper for the Semetric API"),
    long_description=read('README.md'),
    url="http://developer.musicmetric.com",
    license="PSF",
    namespace_packages=['semetric'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose>=1.3.0'],
    classifiers=[],
    zip_safe=False,
    entry_points = {'console_scripts': [
            'semetric-api = semetric.apiclient:main',
        ],
    }
)
