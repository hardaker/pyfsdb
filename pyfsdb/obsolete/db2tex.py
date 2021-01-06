import sys
import pyfsdb.tools.pdb2tex

def main():
    sys.stderr.write("db2tex is obsolete; please use pdb2tex instead\n")
    pyfsdb.tools.pdb2tex.main()


if __name__ == '__main__':
    main()
