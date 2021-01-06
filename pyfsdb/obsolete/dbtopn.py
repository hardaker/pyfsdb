import sys
import pyfsdb.tools.pdbtopn

def main():
    sys.stderr.write("dbtopn is obsolete; please use pdbtopn instead\n")
    pyfsdb.tools.pdbtopn.main()


if __name__ == '__main__':
    main()
