import sys
import pyfsdb.tools.pdbensure

def main():
    sys.stderr.write("dbensure is obsolete; please use pdbensure instead\n")
    pyfsdb.tools.pdbensure.main()


if __name__ == '__main__':
    main()
