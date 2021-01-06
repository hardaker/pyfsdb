import sys
import pyfsdb.tools.pdbdatetoepoch

def main():
    sys.stderr.write("dbdatetoepoch is obsolete; please use pdbdatetoepoch instead\n")
    pyfsdb.tools.pdbdatetoepoch.main()


if __name__ == '__main__':
    main()
