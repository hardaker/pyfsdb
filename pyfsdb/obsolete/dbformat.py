import sys
import pyfsdb.tools.pdbformat

def main():
    sys.stderr.write("dbformat is obsolete; please use pdbformat instead\n")
    pyfsdb.tools.pdbformat.main()


if __name__ == '__main__':
    main()
