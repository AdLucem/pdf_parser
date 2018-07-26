"""Takes a text file (i.e: pdf converted to text)
and removes unnecessary or 'dirtying' data"""

import os
from get_titles import get_flat_title_list
from nltk import word_tokenize

# =============================== FUNCTIONS =============================


def get_lines_to_remove(lines_to_remove):

    """Gets the user-provided list of lines to remove"""

    with open(lines_to_remove, 'r+') as f:
        return f.readlines()


def include(line, remove_anyway, lines_to_remove):

    """Only include a line in the cleaned file if it is not:
    (1) A page number
    (2) Table of contents"""

    line_remove_whitespace = line.rstrip(" ").lstrip(" ")

    # check if it is a page number
    if line_remove_whitespace.rstrip('\n').isdigit():
        return False

    # check if it is one of the user-defined
    # lines to be removed
    if line_remove_whitespace in lines_to_remove:
        return False

    # check the flag for if it is part of
    # the table of contents
    if remove_anyway:
        # print(line)  # TEST
        return False

    return True


def clean(file_text, file_pdf, lines_to_remove):

    print("Cleaning the messy text file...")

    """To strip extraneous data- i.e
    (1) Header and formatting
    (2) Table of contents
    (3) Page numbers
    from text file"""

    cleaned_file = '../cleaned_searchdata.txt'

    f = open(cleaned_file, 'w+')
    f.close()

    # get the list of titles
    titles_list = get_flat_title_list(file_pdf)

    # get the value of line containing first title
    first_title = [titles_list[0][0]] + titles_list[0][1]

    # flag to strip all text until the first title
    remove_anyway = True

    # get user-defined list of lines to remove
    lines_to_remove = get_lines_to_remove(lines_to_remove)

    with open(cleaned_file, 'a+') as cf:
        with open(file_text, 'r+') as f:

            size = os.path.getsize(os.path.abspath(file_text))
            pointer = 0

            # while pointer position is not beyond EOF
            while pointer < size:

                # read a single line at a time
                line = f.readline().decode('utf-8')

                if word_tokenize(line) == first_title:
                    remove_anyway = False

                # only include lines meant to be included
                if include(line, remove_anyway, lines_to_remove):
                    cf.write(line.encode('ascii', 'ignore'))

                # get updated position of the pointer
                pointer = f.tell()

    # return the filepath to the cleaned file
    return cleaned_file
