import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfsdb-hardaker",
    version="1.0.0",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="A python implementation of the flat-file streaming database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gawseed/pyfsdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
)
