import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfsdb",
    version="1.1.13",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="A python implementation of the flat-file streaming database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gawseed/pyfsdb",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            # migrating to pdb prefixes
            'pdbtopn = pyfsdb.tools.dbtopn:main',
            'pdbaugment = pyfsdb.tools.dbaugment:main',
            'bro2fsdb = pyfsdb.tools.bro2fsdb:main',
            'pdbcoluniq = pyfsdb.tools.dbcoluniq:main',
            'pdbfullpivot = pyfsdb.tools.dbfullpivot:main',
            'pdbreversepivot = pyfsdb.tools.dbreversepivot:main',
            'pdbzerofill = pyfsdb.tools.dbzerofill:main',
            'pdbkeyedsort = pyfsdb.tools.dbkeyedsort:main',
            'pdbsplitter = pyfsdb.tools.dbsplitter:main',
            'json2fsdb = pyfsdb.tools.json2fsdb:main',
            'fsdb2json = pyfsdb.tools.fsdb2json:main',
            'fsdb2many = pyfsdb.tools.fsdb2many:main',
            'pdb2tex = pyfsdb.tools.db2tex:main',
            'pdbformat = pyfsdb.tools.dbformat:main',
            'pdbreescape = pyfsdb.tools.dbreescape:main',
            'pdbensure = pyfsdb.tools.dbensure:main',
            'pdbheatmap = pyfsdb.tools.dbheatmap:main',
            'pdbdatetoepoch = pyfsdb.tools.dbdatetoepoch:main',
            'pdbnormalize = pyfsdb.tools.dbnormalize:main',
            'pdbsum = pyfsdb.tools.dbsum:main',

            # obsolete wrappers
            'dbtopn = pyfsdb.obsolete.dbtopn:main',
            'dbaugment = pyfsdb.obsolete.dbaugment:main',
            'dbcoluniq = pyfsdb.obsolete.dbcoluniq:main',
            'dbfullpivot = pyfsdb.obsolete.dbfullpivot:main',
            'dbreversepivot = pyfsdb.obsolete.dbreversepivot:main',
            'dbzerofill = pyfsdb.obsolete.dbzerofill:main',
            'dbkeyedsort = pyfsdb.obsolete.dbkeyedsort:main',
            'dbsplitter = pyfsdb.obsolete.dbsplitter:main',
            'db2tex = pyfsdb.obsolete.db2tex:main',
            'dbformat = pyfsdb.obsolete.dbformat:main',
            'dbreescape = pyfsdb.obsolete.dbreescape:main',
            'dbensure = pyfsdb.obsolete.dbensure:main',
            'dbheatmap = pyfsdb.obsolete.dbheatmap:main',
            'dbdatetoepoch = pyfsdb.obsolete.dbdatetoepoch:main',
            'dbnormalize = pyfsdb.obsolete.dbnormalize:main',
            'dbsum = pyfsdb.obsolete.dbsum:main',
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
