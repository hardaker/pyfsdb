import sys
import pyfsdb.tools.pdbsum

def main():
    sys.stderr.write("dbsum is obsolete; please use pdbsum instead\n")
    pyfsdb.tools.pdbsum.main()


if __name__ == '__main__':
    main()
