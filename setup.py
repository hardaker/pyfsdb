import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfsdb",
    version="0.9.3",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="A python implementation of the flat-file streaming database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gawseed/pyfsdb",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'dbtopn = pyfsdb.topn:main',
            'dbaugment = pyfsdb.augment:main',
            'bro2fsdb = pyfsdb.pro2fsdb:main',
            'dbcoluniq = pyfsdb.coluniq:main',
            'dbfullpivot = pyfsdb.fullpivot:main',
            'dbzerofill = pyfsdb.zerofill:main',
            'dbkeyedsort = pyfsdb.keyedsort:main',
            'dbsplitter = pyfsdb.splitter:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)
