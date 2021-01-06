import sys
import pyfsdb.tools.pdbreversepivot

def main():
    sys.stderr.write("dbreversepivot is obsolete; please use pdbreversepivot instead\n")
    pyfsdb.tools.pdbreversepivot.main()


if __name__ == '__main__':
    main()
