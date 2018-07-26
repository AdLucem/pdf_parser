"""Extract all tables from an html file to a json object
Note: this accounts even for large HTML files"""

import re


def extract_table(filename, start_ptr):

    is_table = False

    with open(filename, 'r+') as f:

        # goto point from where to start reading
        f.seek(start_ptr)
        table_tag = ""

        while True:

            line = f.readline()

            if (not is_table) and ('<TABLE' in line):
                is_table = True

            if is_table and ('</TABLE>' in line):
                table_tag = table_tag + line + '\n'
                break
            elif is_table:
                table_tag = table_tag + line + '\n'

        ptr_at = f.tell()

    return table_tag, ptr_at


def html_table_to_matrix(table_tag):

    lines = table_tag.split('\n')

    matrix = []

    for index, line in enumerate(lines):

        if '<TR>' in line:
            keys = []
            is_row = True
            continue
        elif '</TR>' in line:
            matrix.append(keys)
            is_row = False
            continue
        elif is_row:
            # continue here 1/6/18
            re.sub()









def get_all_tables(filename):

    f = open('../table_normalised.html', 'w+')
    f.close()

    with open('../table_normalised.html', 'a+'):
        pass



