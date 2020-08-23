from unittest import TestCase
import pyfsdb

class FsdbTest(TestCase):
    DATA_FILE = "pyfsdb/tests/tests.fsdb"
    OUT_FILE = "pyfsdb/tests/testout.fsdb"

    def test_loaded_tests(self):
        self.assertTrue(True)

    def test_read_header(self):
        HEADER_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb()
        fileh = open(HEADER_FILE, "r")
        line = next(fileh)
        headers = f.read_header(line)

        self.assertTrue(headers[0] == 0, "header parse is 0 for success")

        header_info = headers[1]

        for colname in ('names', 'numbers', 'header'):
            self.assertTrue(colname in header_info,
                            "header structure contains " + colname)

        names_info = header_info['names']
        numbers_info = header_info['numbers']

        counter = 0
        for column in ('colone', 'coltwo', 'colthree'):
            self.assertTrue(column in names_info,
                            "column info contains data on " + column)
            self.assertTrue(names_info[column] == counter,
                            "column " + column + " is number " + str(counter))

            self.assertTrue(numbers_info[counter] == column,
                            "column number " + str(counter) + " is labeled " + column)

            counter += 1

    def check_data(self, rows):
        self.assertTrue(len(rows) == 2,
                    "There are two rows in the results")

        self.assertTrue(rows[0][0] == 'rowone')
        self.assertTrue(rows[0][1] == 'info')
        self.assertTrue(rows[0][2] == 'data')

        self.assertTrue(rows[1][0] == 'rowtwo')
        self.assertTrue(rows[1][1] == 'other')
        self.assertTrue(rows[1][2] == 'stuff')


    def test_read_all_data(self):
        HEADER_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb()
        fileh = open(HEADER_FILE, "r")
        data = f.read_fsdb(fileh)

        self.assertTrue(data[0] == 0,
                        'parsing status is 0')
        self.assertTrue('data' in data[1],
                        'data is in the output')

        rows = data[1]['data']
        self.check_data(rows)
        
    def test_broken_header(self):
        from io import StringIO
        data = "a,b,c" # pretend we're a csv
        datah = StringIO(data)
        try:
            with pyfsdb.Fsdb(file_handle=datah) as f:
                row = next(f)
                self.assertTrue(False, "shouldn't have gotten here " + str(row))
        except ValueError:
            self.assertTrue(True, "proper exception thrown")
        except Exception as e:
            self.assertTrue(False, "wrong exception thrown: " + str(e))

    def test_reading_as_iterator(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb(DATA_FILE)

        rows = []
        row = next(f)
        self.assertTrue(row, 'row one is returned')
        rows.append(row)

        row = next(f)
        rows.append(row)
        self.assertTrue(row, 'row two is returned')

        self.check_data(rows)

    def test_reading_as_dict_with_next(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb(DATA_FILE, return_type=pyfsdb.RETURN_AS_DICTIONARY)

        row = next(f)
        self.assertTrue(row, 'row one is returned')

        self.assertTrue(row['colone'] == 'rowone')
        self.assertTrue(row['coltwo'] == 'info')
        self.assertTrue(row['colthree'] == 'data')

        row = next(f)
        self.assertTrue(row, 'row two is returned')
        
        self.assertTrue(row['colone'] == 'rowtwo')
        self.assertTrue(row['coltwo'] == 'other')
        self.assertTrue(row['colthree'] == 'stuff')

    def test_setting_fileh(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb()

        self.assertFalse(f.file_handle, "file_handle should not be available")

        fh = open(DATA_FILE, "r")
        self.assertTrue(fh, "file opened manually")
        
        f.file_handle = fh
        self.assertTrue(f.file_handle == fh, "file_handle was set properly")


        row = next(f)
        self.assertTrue(f.__next__ == f._next_as_array, "read type was set")
        self.assertTrue(row, 'row one is returned')
        self.assertTrue(row[0] == 'rowone')

        # create a new object instead
        fh = open(DATA_FILE, "r")
        f = pyfsdb.Fsdb(file_handle = fh)
        
        row = next(f)
        self.assertTrue(row, 'row one is returned')
        self.assertTrue(row[0] == 'rowone')

        # check that it works as an iterator
        fh = open(DATA_FILE, "r")
        f = pyfsdb.Fsdb(file_handle = fh)

        count = 0
        for row in f:
            count += 1

        self.assertTrue(count > 0, "at least one row read")

    def test_header_access(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb(DATA_FILE)
        self.assertTrue(f, "opened ok")

        headers = f.headers
        self.assertTrue(headers, "headers access exists")

        self.assertTrue(f.get_column_name(0) == "colone")
        self.assertTrue(f.get_column_name(1) == "coltwo")
        self.assertTrue(f.get_column_name(2) == "colthree")
        self.assertTrue(f.get_column_number("colone") == 0)
        self.assertTrue(f.get_column_number("coltwo") == 1)
        self.assertTrue(f.get_column_number("colthree") == 2)

        self.assertTrue(f.header_line == "#fsdb -F t colone coltwo colthree\n")

        cols = f.column_names
        self.assertTrue(len(cols) == 3, "There are two cloumns")
        self.assertTrue(cols[0] == "colone", "column one ok")
        self.assertTrue(cols[1] == "coltwo", "column two ok")
        self.assertTrue(cols[2] == "colthree", "column three ok")
        self.assertTrue(cols[2] == "colthree", "column three ok")
        self.assertTrue(f.column_names[2] == "colthree", "column three ok")

    def test_output(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        f = pyfsdb.Fsdb(DATA_FILE)
        self.assertTrue(f, "opened ok")

        expected = [
            "rowone	info	data\n",
            "rowtwo	other	stuff\n",
        ]
        
        for row in f:
            output_string = f.row_as_string()
            self.assertTrue(expected[0] == output_string,
                            "output string " + output_string + " ok")
            expected = expected[1:]

    def test_setting_columns(self):
        f = pyfsdb.Fsdb()
        self.assertTrue(f, "opened ok")
        
        testcols = ['colone','coltwo','col3']
        f.column_names = testcols
        self.assertTrue(f.column_names == testcols)

    def test_header(self):
        f = pyfsdb.Fsdb()
        self.assertTrue(f, "opened ok")
        
        f.column_names = ['colone','coltwo','col3']
        self.assertTrue(f.header_line == "#fsdb -F t colone coltwo col3\n")

        old = list(f.column_names)
        old.append('col4')
        f.column_names = old
        self.assertTrue(f.header_line == "#fsdb -F t colone coltwo col3 col4\n")

        f.separator_token = "S"
        self.assertTrue(f.header_line == "#fsdb -F S colone coltwo col3 col4\n")

        f.separator = " "
        self.assertTrue(f.header_line == "#fsdb -F s colone coltwo col3 col4\n")

    def test_missing_header_support_file(self):
        DATA_FILE = "pyfsdb/tests/noheader.fsdb"
        f = pyfsdb.Fsdb(DATA_FILE)
        self.assertTrue(f, "opened ok")
        f.column_names = ['colone', 'coltwo', 'colthree']

        headers = f.headers
        self.assertTrue(headers, "headers access exists")

        self.assertTrue(f.get_column_name(0) == "colone")
        self.assertTrue(f.get_column_name(1) == "coltwo")
        self.assertTrue(f.get_column_name(2) == "colthree")
        self.assertTrue(f.get_column_number("colone") == 0)
        self.assertTrue(f.get_column_number("coltwo") == 1)
        self.assertTrue(f.get_column_number("colthree") == 2)

        self.assertTrue(f.header_line == "#fsdb -F t colone coltwo colthree\n")

        cols = f.column_names
        self.assertTrue(len(cols) == 3, "There are two cloumns")
        self.assertTrue(cols[0] == "colone", "column one ok")
        self.assertTrue(cols[1] == "coltwo", "column two ok")
        self.assertTrue(cols[2] == "colthree", "column three ok")
        self.assertTrue(cols[2] == "colthree", "column three ok")
        self.assertTrue(f.column_names[2] == "colthree", "column three ok")

    def test_missing_header_support_filehandle(self):
        from io import StringIO
        data = "a	b	c\n"
        datah = StringIO(data)
        f = pyfsdb.Fsdb(file_handle=datah)
        self.assertTrue(f, "opened ok")
        f.column_names = (["a", "b", "c"])

        self.assertTrue(f.get_column_name(0) == "a")
        self.assertTrue(f.get_column_name(1) == "b")
        self.assertTrue(f.get_column_name(2) == "c")
        self.assertTrue(f.get_column_number("a") == 0)
        self.assertTrue(f.get_column_number("b") == 1)
        self.assertTrue(f.get_column_number("c") == 2)

        self.assertTrue(f.header_line == "#fsdb -F t a b c\n")


    def test_write_out_fsdb(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        OUT_FILE = "pyfsdb/tests/testout.fsdb"

        f = pyfsdb.Fsdb(DATA_FILE, out_file = OUT_FILE)
        self.assertTrue(f, "opened ok")

        # read in all records
        records = []
        for record in f:
            records.append(record)

        self.assertTrue(records[0][0] == 'rowone',
                        'init record ' + records[0][0] + ' is correct')

        for record in records:
            f.write_row(record)

        f.write_finish()

        g = pyfsdb.Fsdb(OUT_FILE)
        rows = []
        for row in g:
            rows.append(row)
        self.check_data(rows)

        # write out new columns
        f = pyfsdb.Fsdb(out_file = OUT_FILE)
        count = 1

        f.out_column_names = ['a','b','c','new_count']
        self.assertTrue(len(f.out_column_names) == 4,
                        "correct initial output count")
        for row in rows:
            row.append(str(count))
            f.write_row(row)
            count = count + 1
        f.write_finish()

        # check new columns
        g = pyfsdb.Fsdb(filename = OUT_FILE)
        rows = []
        for row in g:
            rows.append(row)
        self.check_data(rows)
        self.assertTrue(rows[0][3] == "1", "new rowone col is correct")
        self.assertTrue(rows[1][3] == "2", "new rowtwo col is correct")

        # check the output token switch
        f = pyfsdb.Fsdb(DATA_FILE, out_file = OUT_FILE)
        self.assertTrue(f, "opened ok")
        f.out_separator_token = "s"
        self.assertTrue(f.out_separator == ' ', "new separator is space")
        for row in f:
            f.write_row(row)
        f.write_finish()

    def check_last_line(self, outfile, lastline):
        saved = open(outfile, "r")
        foundIt = False
        wasLast = False
        for line in saved:
            if line == lastline:
                foundIt = True
                wasLast = True
            else:
                wasLast = False
        self.assertTrue(foundIt, "saved output command")
        self.assertTrue(wasLast, "saved command was last")

    def test_out_command_line(self):

        f = pyfsdb.Fsdb(self.DATA_FILE, out_file = self.OUT_FILE)
        self.assertTrue(f, "opened ok")

        f.out_command_line = "test command"
        f.write_finish()

        self.check_last_line(self.OUT_FILE, "#   | test command\n")

    def test_save_out_command_on_del(self):
        f = pyfsdb.Fsdb(self.DATA_FILE, out_file = self.OUT_FILE)
        self.assertTrue(f, "opened ok")

        f.out_command_line = "test command on del"
        del f

        self.check_last_line(self.OUT_FILE, "#   | test command on del\n")

    def test_dont_save_command(self):
        f = pyfsdb.Fsdb(out_file = self.OUT_FILE)
        f.out_command_line = None
        f.out_file_handle.write("#   | test nowrite\n")
        del f

        self.check_last_line(self.OUT_FILE, "#   | test nowrite\n")

    def test_save_out_command_from_init(self):
        f = pyfsdb.Fsdb(self.DATA_FILE, out_file = self.OUT_FILE,
                      out_command_line = "test command init")
        self.assertTrue(f, "opened ok")
        del f

        self.check_last_line(self.OUT_FILE, "#   | test command init\n")

    def test_comments_passed_inline(self):
        out_file = self.OUT_FILE
        f = pyfsdb.Fsdb(self.DATA_FILE, out_file = out_file,
                      out_command_line = "test command init")
        self.assertTrue(f, "opened ok")
        for row in f:
            f.write_row(row)
        f.write_finish()
		
        lines = []
        f = open(out_file, "r")
        for line in f:
            lines.append(line)

        self.assertTrue(lines[len(lines)-1] == "#   | test command init\n")
        self.assertTrue(lines[len(lines)-2] == "# | manually generated\n")
        self.assertTrue(lines[len(lines)-3] == "rowtwo	other	stuff\n")
        self.assertTrue(lines[len(lines)-4] == "# middle comment\n")

    def test_comments_passed_at_end(self):
        out_file = self.OUT_FILE
        f = pyfsdb.Fsdb(self.DATA_FILE, out_file = out_file,
                      out_command_line = "test command init",
					  pass_comments = 'e')
        self.assertTrue(f, "opened ok")
        for row in f:
            f.write_row(row)
        f.write_finish()
		
        lines = []
        f = open(out_file, "r")
        for line in f:
            lines.append(line)

        self.assertTrue(lines[len(lines)-1] == "#   | test command init\n")
        self.assertTrue(lines[len(lines)-2] == "# | manually generated\n")
        self.assertTrue(lines[len(lines)-3] == "# middle comment\n")
        self.assertTrue(lines[len(lines)-4] == "rowtwo	other	stuff\n")

    def test_array_generator(self):
        f = pyfsdb.Fsdb(self.DATA_FILE)
        self.assertTrue(f, "opened ok")

        all = []
        for r in f.next_as_array():
            all.append(r)

        self.check_data(all)

    def test_dict_generator(self):
        f = pyfsdb.Fsdb(self.DATA_FILE)
        self.assertTrue(f, "opened ok")

        # this generally shouldn't be called as is, so we need to self-init
        f.maybe_open_filehandle()
        f.read_header()

        all = []
        for r in f.next_as_dict():
            all.append(r)

        self.check_data([[all[0]['colone'], all[0]['coltwo'], all[0]['colthree']],
                         [all[1]['colone'], all[1]['coltwo'], all[1]['colthree']]])

    def test_get_pandas(self):
        f = pyfsdb.Fsdb(self.DATA_FILE)
        self.assertTrue(f, "opened ok")
        
        all = f.get_pandas()
        self.check_data(all.values.tolist())

    def test_get_pandas(self):
        f = pyfsdb.Fsdb(self.DATA_FILE)
        self.assertTrue(f, "opened ok")
        
        all = f.get_pandas(usecols=['coltwo'])
        rows = all.values.tolist()
        self.assertTrue(len(rows) == 2)
        self.assertTrue(len(rows[0]) == 1)
        self.assertTrue(len(rows[1]) == 1)
        self.assertTrue(rows[0][0] == "info")
        self.assertTrue(rows[1][0] == "other")
        
    def test_comment_ordering(self):
        HEADER_FILE = "pyfsdb/tests/test_comments_at_top.fsdb"
        OUTPUT_FILE = "pyfsdb/tests/test_comments_at_top.test.fsdb"
        f = pyfsdb.Fsdb(filename=HEADER_FILE, out_file=OUTPUT_FILE)
        for row in f:
            f.write_row(row)
        f.write_finish()

        # the headers should fail
        self.assertTrue(True, "got here")

        # load both files fully
        file1 = ""
        with open(HEADER_FILE, "r") as fh:
            file1 = fh.read(8192)
            
        file2 = ""
        with open(OUTPUT_FILE, "r") as fh:
            file2 = fh.read(8192)

        print("file2:" + file2)

        self.assertTrue(file2.startswith(file1), # ignore added trailers
                         "file contents with headers are the same")

    def test_with_usage(self):
        DATA_FILE = "pyfsdb/tests/tests.fsdb"
        with pyfsdb.Fsdb(DATA_FILE) as f:
            row = next(f)
            self.assertTrue(row, 'row one is returned')

            self.assertTrue(row[0] == 'rowone')
            self.assertTrue(row[1] == 'info')
            self.assertTrue(row[2] == 'data')

    def test_missing_columns(self):
        from io import StringIO
        data = "#fsdb -F t a b c\n1\t2\t3\n4\t5\n"
        datah = StringIO(data)
        with pyfsdb.Fsdb(file_handle=datah) as f:
            r1 = next(f)

            self.assertEqual(f.column_names, ['a', 'b', 'c'],
                             "column names are right")
            self.assertEqual(r1, ['1','2','3'],
                             "column values for row 1 are correct")

            r2 = next(f)
            self.assertEqual(r2, ['4', '5', ''],
                             "column values for row 2 are correct")
            
    def test_broken_data(self):
        from io import StringIO
        data = "a,b,c" # pretend we're a csv
        datah = StringIO(data)
        try:
            with pyfsdb.Fsdb(file_handle=datah) as f:
                row = next(f)
                self.assertTrue(False, "shouldn't have gotten here")
        except ValueError:
            self.assertTrue(True, "proper exception thrown")
        except Exception as e:
            self.assertTrue(False, "wrong exception thrown: " + str(e))

    def test_foreach(self):
        from io import StringIO
        data = "#fsdb -F t a b c\n1\t2\t3\n4\t5\t6\n"
        datah = StringIO(data)
        with pyfsdb.Fsdb(file_handle=datah,
                         return_type=pyfsdb.RETURN_AS_DICTIONARY) as f:
            ret = f.foreach(lambda x: x['b'])
            self.assertEqual(ret, ['2', '5'],
                             "foreach response data is correct")
        

    def test_filter(self):
        from io import StringIO
        data = "#fsdb -F t a b c\n1\t2\t3\n4\t5\t6\n"
        datah = StringIO(data)

        def double_middle(row):
            row[1] = 2*int(row[1])
            return(row)

        outh = StringIO()
        f = pyfsdb.Fsdb(file_handle=datah,
                        out_file_handle=outh)
        f.filter(double_middle)

        self.assertEqual(outh.getvalue(),
                         "#fsdb -F t a b c\n1\t4\t3\n4\t10\t6\n",
                         "filter properly double the middle column")

        f.close()

    def test_filter_with_args(self):
        from io import StringIO
        data = "#fsdb -F t a b c\n1\t2\t3\n4\t5\t6\n"
        datah = StringIO(data)

        def double_middle(row, by):
            row[1] = by*int(row[1])
            return(row)

        outh = StringIO()
        f = pyfsdb.Fsdb(file_handle=datah,
                        out_file_handle=outh)
        f.filter(double_middle, args=[2])

        self.assertEqual(outh.getvalue(),
                         "#fsdb -F t a b c\n1\t4\t3\n4\t10\t6\n",
                         "filter properly double the middle column")

        f.close()

    def test_filter_with_writing_dictionaries(self):
        from io import StringIO
        data = "#fsdb -F t a b c\n1\t2\t3\nskip\t\tblanks\n4\t5\t6\n"
        datah = StringIO(data)

        def double_middle_dict(row):
            if row['b'] == '': # tests returning no-entries drops it
                return
            row['b'] = 2*int(row['b'])
            return(row)

        outh = StringIO()
        f = pyfsdb.Fsdb(file_handle=datah,
                        out_file_handle=outh,
                        return_type=pyfsdb.RETURN_AS_DICTIONARY)
        f.filter(double_middle_dict)

        self.assertEqual(outh.getvalue(),
                         "#fsdb -F t a b c\n1\t4\t3\n4\t10\t6\n",
                         "filter properly double the middle column")

        f.close()
if __name__ == "__main__":
    unittest.main()
        


