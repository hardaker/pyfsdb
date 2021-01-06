import sys
import pyfsdb.tools.pdbfullpivot

def main():
    sys.stderr.write("dbfullpivot is obsolete; please use pdbfullpivot instead\n")
    pyfsdb.tools.pdbfullpivot.main()


if __name__ == '__main__':
    main()
