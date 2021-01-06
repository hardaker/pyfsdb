import sys
import pyfsdb.tools.pdbreescape

def main():
    sys.stderr.write("dbreescape is obsolete; please use pdbreescape instead\n")
    pyfsdb.tools.pdbreescape.main()


if __name__ == '__main__':
    main()
