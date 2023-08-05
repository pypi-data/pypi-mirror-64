from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = open('requirements.txt').read().split('\n')
install_requires = install_requires,


setup(
    name='familiar',
    version='0.0.8',
    description='Dungeons and Dragons helper functions',
    # py_modules=['familiar'],
    # package_dir={'': 'src'},
    packages=['src'],
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
