import sys
import pyfsdb.tools.pdbaugment

def main():
    sys.stderr.write("dbaugment is obsolete; please use pdbaugment instead\n")
    pyfsdb.tools.pdbaugment.main()


if __name__ == '__main__':
    main()
