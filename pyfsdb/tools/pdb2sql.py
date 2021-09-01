#!/usr/bin/python3

"""Convert an FSDB file into a sqlite3 database"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import sqlite3
import pyfsdb


def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: db2sql input.fsdb output.sqlite3")

    parser.add_argument("-c", "--converters", default=[], type=str, nargs='*',
                        help="Convert column names to these sql types.  Arguments should be name/type pairs separated by equal signs")

    parser.add_argument("--delete", "--delete-existing-rows", action="store_true",
                        help="Delete existing data before inserting new rows (ie, replace the data)")

    parser.add_argument("--log-level", default="info",
                        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).")

    parser.add_argument("-i", "--indexes", default=[], type=str, nargs="*",
                        help="Index columns to use when creating the table")

    parser.add_argument("-e", "--extra-columns", default=[], type=str, nargs="*",
                        help="Extra column specifiers to use when creating a table in name=type format")

    parser.add_argument("-v", "--extra-values", default=[], type=str, nargs="*",
                        help="Extra column values to use when inserting data")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="Input fsdb file to load")

    parser.add_argument("output_file", type=str,
                        nargs='?', help="Output sqlite3 to create or augment")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level,
                        format="%(levelname)-10s:\t%(message)s")
    return args


class FsdbSqlite3():
    def __init__(self, fsdb_handle, output_sqlite3_filename, **kwargs):
        self.fsdb = pyfsdb.Fsdb(file_handle=fsdb_handle, **kwargs)
        self.con = sqlite3.connect(output_sqlite3_filename)
        self.cur = self.con.cursor()

        self.table_name = "fsdb_table"
        if 'table_name' in kwargs:
            self.table_name = kwargs['table_name']
            del kwargs['table_name']

        self.converters = {}
        if 'converters' in kwargs:
            self.table_name = kwargs['converters']

    def create_table(self, indexes=[], table_name="fsdb_table", extra_columns=[]):
        "creates a new database from a definition within an FSDB handle"
        columns = self.fsdb.column_names

        column_strings = []
        for column in columns:
            coltype = self.converters.get(column, 'string')
            column_strings.append(f"{column} {coltype}")

        self.table_name = table_name

        # see if we have extra columns to add
        extra_columns_str = ""
        if extra_columns:
            transformed = []
            for spec in extra_columns:
                pair = spec.split("=")
                transformed.append(" ".join(pair))
            extra_columns_str = ", ".join(transformed) + ","

        # create the table
        statement = f"create table if not exists {table_name} ({extra_columns_str} {', '.join(column_strings)})"
        debug(statement)
        self.con.execute(statement)

        # create any indexes
        for index in indexes:
            parts = index.split(",")
            idx_name = "idx_" + "_".join(parts)
            cols = ", ".join(parts)
            statement = f"create index if not exists {idx_name} on {table_name} ({cols})"
            debug(statement)
            self.con.execute(statement)

    def insert_into_to_table(self, extra_values=[], chunks=100):
        """Insert the rows of the database into the sqlite3 table"""

        extra_columns_str = ""
        extra_vals = []
        if extra_values:
            extra_cols = []
            extra_vals = []
            for spec in extra_values:
                pair = spec.split("=")
                extra_cols.append(pair[0])
                extra_vals.append(f"{pair[1]}")
            extra_columns_str = ", ".join(extra_cols) + ","

        statement = f"insert into {self.table_name} ({extra_columns_str} {','.join(self.fsdb.column_names)}) " + \
            f"values({','.join(['?'] * (len(extra_vals) + len(self.fsdb.column_names)))})"
        debug(statement)

        self.cur.execute('begin transaction')
        for n, row in enumerate(self.fsdb):
            self.cur.execute(statement, extra_vals + row)
            if (n % chunks == 0):
                self.cur.execute("end transaction")
                self.cur.execute("begin transaction")
                self.con.commit()
        self.cur.execute("end transaction")
        self.con.commit()

    def clear_table(self):
        """Deletes existing rows from the table"""
        self.con.execute(f"delete from {self.table_name}")
        self.con.commit()


def main():
    args = parse_args()

    conv = FsdbSqlite3(args.input_file, args.output_file,
                       converters=args.converters)
    conv.create_table(indexes=args.indexes, extra_columns=args.extra_columns)
    if args.delete:
        conv.clear_table()
    conv.insert_into_to_table(args.extra_values)


if __name__ == "__main__":
    main()
