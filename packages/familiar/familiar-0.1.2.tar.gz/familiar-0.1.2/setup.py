from setuptools import setup
import re
import os
import sys


with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = open('requirements.txt').read().split('\n')


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='familiar',
    version='0.1.2',
    description='Dungeons and Dragons helper functions',
    py_modules=['familiar'],
    # package_dir={'': 'familiar_tools'},
    packages=get_packages('familiar_tools'),
    package_data=get_package_data('familiar_tools'),
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Role-Playing"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JDSalisbury/familiar",
    author='Jeff Salisbury',
    author_email='pip.familiar@gmail.com'
)
