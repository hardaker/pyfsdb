import sys
import pyfsdb.tools.pdbcoluniq

def main():
    sys.stderr.write("dbcoluniq is obsolete; please use pdbcoluniq instead\n")
    pyfsdb.tools.pdbcoluniq.main()


if __name__ == '__main__':
    main()
