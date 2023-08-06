from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'get-prime-number',
    version = '0.1',
    description = 'A prime number generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Ariel Barcellos',
    author_email = 'contact@arielbarcellos.com',
    url = 'https://github.com/naijopkr/get-prime-number',
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3.0',
)
