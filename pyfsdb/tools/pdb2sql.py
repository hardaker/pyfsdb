#!/usr/bin/python3

"""Convert an FSDB file into a sqlite3 database"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import pyfsdb


def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: db2sql input.fsdb output.sqlite3",
    )

    parser.add_argument(
        "-c",
        "--converters",
        default=[],
        type=str,
        nargs="*",
        help="Convert column names to these sql types.  Arguments should be name/type pairs separated by equal signs",
    )

    parser.add_argument(
        "--delete",
        "--delete-existing-rows",
        action="store_true",
        help="Delete existing data before inserting new rows (ie, replace the data)",
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "-i",
        "--indexes",
        default=[],
        type=str,
        nargs="*",
        help="Index columns to use when creating the table",
    )

    parser.add_argument(
        "-e",
        "--extra-columns",
        default=[],
        type=str,
        nargs="*",
        help="Extra column specifiers to use when creating a table in name=type format",
    )

    parser.add_argument(
        "-v",
        "--extra-values",
        default=[],
        type=str,
        nargs="*",
        help="Extra column values to use when inserting data",
    )

    parser.add_argument(
        "-t",
        "--database-type",
        default="sqlite3",
        type=str,
        help="Type of database to use (sqlite3, pg, maria, print)",
    )

    parser.add_argument(
        "-H",
        "--database-hostname",
        default=None,
        type=str,
        help="Hostname to connect to for host-based datatypes",
    )

    parser.add_argument(
        "-U",
        "--database-user",
        default=None,
        type=str,
        help="Database user name to connect with for host-based datatypes",
    )

    parser.add_argument(
        "-P",
        "--database-password",
        default=None,
        type=str,
        help="Database password to connect with for host-based datatypes",
    )

    parser.add_argument(
        "-T",
        "--table-name",
        default="fsdb_table",
        type=str,
        help="The table name to create",
    )

    parser.add_argument(
        "input_file",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="Input fsdb file to load",
    )

    parser.add_argument(
        "database_name",
        type=str,
        nargs="?",
        default="database.fsdb",
        help="Output sqlite3 file or database name to use",
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")
    return args


class FsdbSql:
    def __init__(self, fsdb_handle, **kwargs):
        self.arguments = kwargs

        # extract various parameters from the CLI arguments
        self.table_name = self.get_and_remove_value("table_name", kwargs, "fsdb_table")
        self.database_name = self.get_and_remove_value("database_name", kwargs, "fsdb")
        self.database_hostname = self.get_and_remove_value("database_hostname", kwargs)
        self.database_user = self.get_and_remove_value("database_user", kwargs)
        self.database_password = self.get_and_remove_value("database_password", kwargs)

        # set up type converter list
        self.converters = {}
        if "converters" in kwargs:
            for converter in kwargs["converters"]:
                (key, converter_type) = converter.split("=")
                self.converters[key] = converter_type
            debug(f"created converters: {self.converters}")
            kwargs["converters"] = self.converters

        self.data_types = {
            int: "integer",
            str: "string",
            float: "float",
        }
        self.param_string = "?"

        # bootstrap the database and input file
        self.get_cursor()
        self.fsdb = pyfsdb.Fsdb(file_handle=fsdb_handle)  # , **kwargs

    def get_and_remove_value(self, name, kwargs, default=None):
        if name in kwargs:
            default = kwargs[name]
            del kwargs[name]
        return default

    def get_datatype(self, from_column):
        # see if we have a user specified type to use:
        coltype = self.converters.get(from_column, None)

        # else pull the datatype from the fsdb(v2) handle if possible:
        if not coltype and self.fsdb.converters:
            # this returns a python type converter (str, int, etc)
            coltype = self.fsdb.converters.get(from_column, str)

        if coltype in self.data_types:
            # from the type, get the database string representation
            coltype = self.data_types[coltype]

        if not coltype:
            return self.data_types[str]

        return coltype

    def get_cursor(
        self,
    ):
        error("illegal base table usage")

    def create_table(self, indexes=[], extra_columns=[]):
        "creates a new database from a definition within an FSDB handle"
        table_name = self.table_name
        columns = self.fsdb.column_names

        column_strings = []
        for column in columns:
            coltype = self.get_datatype(column)
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
        self.execute(statement)

        # create any indexes
        for index in indexes:
            parts = index.split(",")
            idx_name = "idx_" + "_".join(parts)
            cols = ", ".join(parts)
            statement = (
                f"create index if not exists {idx_name} on {table_name} ({cols})"
            )
            debug(statement)
            self.execute(statement)

    def insert_into_to_table(self, extra_values=[], chunks=10000, drop_columns=[]):
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

        column_names = []
        for col in self.fsdb.column_names:
            if col not in drop_columns:
                column_names.append(col)

        column_nums = self.fsdb.get_column_numbers(column_names)

        statement = (
            f"insert into {self.table_name} ({extra_columns_str}{','.join(column_names)}) "
            + f"values({','.join([self.param_string] * (len(extra_vals) + len(column_names)))})"
        )
        debug(statement)

        self.execute("begin transaction")
        for n, row in enumerate(self.fsdb):
            vals = [row[x] for x in column_nums]
            self.execute(statement, extra_vals + vals)
            if n % chunks == 0:
                self.execute("end transaction")
                self.execute("begin transaction")
                self.commit()
        if n % chunks != 0:
            # (if it's zero we just created the transaction)
            self.execute("end transaction")
        self.commit()

    def clear_table(self):
        """Deletes existing rows from the table"""
        self.execute(f"delete from {self.table_name}")
        self.commit()

    def execute(self, *args, **kwargs):
        self.cur.execute(*args, **kwargs)

    def commit(self, *args, **kwargs):
        self.con.commit(*args, **kwargs)


class FsdbSqlite3(FsdbSql):
    def get_cursor(self):
        import sqlite3

        self.con = sqlite3.connect(self.database_name)
        self.cur = self.con.cursor()


class PgSql(FsdbSql):
    def get_cursor(self):
        import psycopg2

        self.data_types[str] = "text"
        self.param_string = "%s"

        self.con = psycopg2.connect(
            database=self.database_name,
            user=self.database_user,
            password=self.database_password,
            host=self.database_hostname,
        )
        self.cur = self.con.cursor()


class FsdbSqlPrint(FsdbSql):
    "A wrapper to just print the resulting output of sql statements"

    def get_cursor(self):
        self.con = self
        self.cur = self
        return self

    def execute(self, statement, values=[]):
        print(statement)
        if values:
            sys.stdout.write("  ")
            print(values)

    def commit(self):
        print("# commit")


def main():
    args = parse_args()

    if args.database_type == "sqlite3":
        conv = FsdbSqlite3(
            args.input_file,
            database_name=args.database_name,
            table_name=args.table_name,
            converters=args.converters,
        )
    elif args.database_type == "pg":
        conv = PgSql(
            args.input_file,
            table_name=args.table_name,
            database_name=args.database_name,
            database_user=args.database_user,
            database_password=args.database_password,
            database_hostname=args.database_hostname,
            converters=args.converters,
        )
    elif args.database_type == "print":
        conv = FsdbSqlPrint(
            args.input_file,
            table_name=args.table_name,
            database_name=args.database_name,
            converters=args.converters,
        )
    else:
        error("unsupported database type: {args.database_type}")

    conv.create_table(indexes=args.indexes, extra_columns=args.extra_columns)
    if args.delete:
        conv.clear_table()
    conv.insert_into_to_table(args.extra_values)


if __name__ == "__main__":
    main()
