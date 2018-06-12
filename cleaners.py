"""Cleans the text document so that it is ready to be processed"""


import os
from build_title_tree import return_title_graph, Tree, flatten
from nltk import word_tokenize

# =============================== FUNCTIONS =============================


def get_titles(filename):

    """Fetch a list of titles in the format:
    (<serial number>, <list of tokens in title>, <title without serial number>)
    from the original pdf file"""

    graph = return_title_graph(filename)
    ls = Tree.tree_to_list(graph)
    ls = flatten(ls)
    ls.pop(0)
    return ls


def get_lines_to_remove():

    """Gets the user-provided list of lines to remove"""

    with open('../lines_to_remove.txt', 'r+') as f:
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


def clean(filename):

    print("Cleaning the messy text file...")

    """To strip extraneous data- i.e
    (1) Header and formatting
    (2) Table of contents
    (4) Page numbers
    from text file"""

    relative_filepath = '../' + filename
    cleaned_file = '../cleaned_' + filename

    f = open(cleaned_file, 'w+')
    f.close()

    # get the list of titles
    titles_list = get_titles(relative_filepath.rstrip('txt') + 'pdf')

    # get the value of line containing first title
    first_title = [titles_list[0][0]] + titles_list[0][1]

    # flag to strip all text until the first title
    remove_anyway = True

    # get user-defined list of lines to remove
    lines_to_remove = get_lines_to_remove()

    with open(cleaned_file, 'a+') as cf:
        with open(relative_filepath, 'r+') as f:

            size = os.path.getsize(os.path.abspath(relative_filepath))
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

    # return the filename of the cleaned file
    return cleaned_file
