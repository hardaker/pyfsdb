import sys
import pyfsdb.tools.pdbsplitter

def main():
    sys.stderr.write("dbsplitter is obsolete; please use pdbsplitter instead\n")
    pyfsdb.tools.pdbsplitter.main()


if __name__ == '__main__':
    main()
