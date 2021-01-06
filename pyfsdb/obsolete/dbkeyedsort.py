import sys
import pyfsdb.tools.pdbkeyedsort

def main():
    sys.stderr.write("dbkeyedsort is obsolete; please use pdbkeyedsort instead\n")
    pyfsdb.tools.pdbkeyedsort.main()


if __name__ == '__main__':
    main()
