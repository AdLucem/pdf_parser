"""Take a PDF file as input and build a hierarchical tree of
titles in the file"""

import PyPDF2
from nltk import word_tokenize
from title_tree import Tree

# ============================ FUNCTIONS ==================================


def make_tree(mat, root, previous_node, length_of_bullet):

    """Taking the root node and a list of titles,
    construct a title tree."""

    # if title-list has not been fully traversed yet
    # note: the title-list is tokenised and then passed
    # to the function
    if mat != []:

        # fetch topmost title in list
        title = mat[0][2]
        # fetch topmost tokenised title list
        tokenised_title = mat[0][1]
        # fetch the serial number of the title (also tokenised)
        serial_number = mat[0][0]
        # fetch the full serial number
        str_sno = map(lambda x: str(x), serial_number)
        sno = ".".join(str_sno).rstrip('.')

        # add on current level
        if length_of_bullet == len(serial_number):

            new_node = Tree(sno,
                            tokenised_title,
                            title)
            root.add_child(new_node)
            mat.pop(0)
            make_tree(mat, root, new_node, length_of_bullet)

        # add as child of previously added node
        elif length_of_bullet < len(serial_number):

            new_node = Tree(sno,
                            tokenised_title,
                            title)
            previous_node.add_child(new_node)
            mat.pop(0)
            make_tree(mat, previous_node, new_node, length_of_bullet + 1)

        # go one step up
        elif length_of_bullet > len(serial_number):
            make_tree(mat, root.parent,
                      previous_node, length_of_bullet - 1)

    else:
        return


def flatten(ls):

    """To flatten a list without losing elements
    Args:
    <ls> : list"""

    l_flat = []

    for i in ls:
        if isinstance(i, list):
            l_flat.extend(flatten(i))
        else:
            l_flat.append(i)
    return l_flat


def return_title_graph(title):

    """Creating a graph of PDF titles
    and returning root node of the
    graph"""

    # creating a pdf file object
    pdfFileObj = open(title, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    outlines = pdfReader.getOutlines()

    # closing the file object
    pdfFileObj.close()

    # flatten the lists-within-lists of outlines
    outlines = flatten(outlines)

    matrix = []

    # making a matrix of titles/serial numbers
    for dest in outlines:
        row = []
        title_split = word_tokenize(dest.title)
        row.append(map(lambda x: int(x), title_split[0].split(".")))
        title_split.pop(0)
        row.append(title_split)
        row.append(" ".join(dest.title.split(" ")[1:]))
        matrix.append(row)

    # making a tree out of above matrix
    root = Tree('', [], "")
    make_tree(matrix, root, root, 0)

    # return statement
    return root
