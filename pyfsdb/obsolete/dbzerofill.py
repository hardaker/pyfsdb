import sys
import pyfsdb.tools.pdbzerofill

def main():
    sys.stderr.write("dbzerofill is obsolete; please use pdbzerofill instead\n")
    pyfsdb.tools.pdbzerofill.main()


if __name__ == '__main__':
    main()
