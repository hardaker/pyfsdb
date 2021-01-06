import sys
import pyfsdb.tools.pdbnormalize

def main():
    sys.stderr.write("dbnormalize is obsolete; please use pdbnormalize instead\n")
    pyfsdb.tools.pdbnormalize.main()


if __name__ == '__main__':
    main()
