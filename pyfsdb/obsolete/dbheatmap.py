import sys
import pyfsdb.tools.pdbheatmap

def main():
    sys.stderr.write("dbheatmap is obsolete; please use pdbheatmap instead\n")
    pyfsdb.tools.pdbheatmap.main()


if __name__ == '__main__':
    main()
