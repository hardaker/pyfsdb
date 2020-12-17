import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfsdb",
    version="1.1.12",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="A python implementation of the flat-file streaming database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gawseed/pyfsdb",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'dbtopn = pyfsdb.dbtopn:main',
            'dbaugment = pyfsdb.dbaugment:main',
            'bro2fsdb = pyfsdb.bro2fsdb:main',
            'dbcoluniq = pyfsdb.dbcoluniq:main',
            'dbfullpivot = pyfsdb.dbfullpivot:main',
            'dbreversepivot = pyfsdb.dbreversepivot:main',
            'dbzerofill = pyfsdb.dbzerofill:main',
            'dbkeyedsort = pyfsdb.dbkeyedsort:main',
            'dbsplitter = pyfsdb.dbsplitter:main',
            'json2fsdb = pyfsdb.json2fsdb:main',
            'fsdb2json = pyfsdb.fsdb2json:main',
            'fsdb2many = pyfsdb.fsdb2many:main',
            'db2tex = pyfsdb.db2tex:main',
            'dbformat = pyfsdb.dbformat:main',
            'dbreescape = pyfsdb.dbreescape:main',
            'dbensure = pyfsdb.dbensure:main',
            'dbheatmap = pyfsdb.dbheatmap:main',
            'dbdatetoepoch = pyfsdb.dbdatetoepoch:main',
            'dbnormalize = pyfsdb.dbnormalize:main',
            'dbsum = pyfsdb.dbsum:main',
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
