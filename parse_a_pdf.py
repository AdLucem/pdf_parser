"""Utility functions to help in parsing a pdf document"""

import PyPDF2
import sys
import unicodedata
from nltk import word_tokenize
from bs4 import BeautifulSoup


class Tree:

    """Class to implement a title tree"""
    # int, list
    def __init__(self, nodeNum, nodeKey, originalTitle):

        self.id = nodeNum
        self.key = nodeKey
        self.original = originalTitle
        self.parent = 0
        self.children = []

    def add_child(self, childNode):
        self.children.append(childNode)
        childNode.parent = self

    @staticmethod
    def display(root):

        if not root:
            return

        node = root
        l_num = []
        while node.id != 0:
            l_num.append(node.id)
            node = node.parent
        l_num.reverse()

        for i in l_num:
            print str(i),
        print " :: ", root.key

        if root.children == []:
            return
        else:
            for i in root.children:
                Tree.display(i)

    @staticmethod
    def tree_to_list(root):
        """Convert a tree to a flat list"""

        if not root:
            return []

        node = root
        l_num = []

        while node.id != 0:
            l_num.append(node.id)
            node = node.parent
        num = ""
        l_num.reverse()
        for i in l_num:
            num = num + str(i) + "."
        num = num.rstrip('.')

        if root.children == []:
            return [(num, root.key, root.original)]
        else:
            return [Tree.tree_to_list(i) for i in root.children]


# functions


def make_tree(mat, root, previous_node, lengthList):

    if mat != []:

        cur = mat[0]

        # add on current level
        if lengthList == len(cur[0]):
            new_node = Tree(cur[0][lengthList - 1], cur[1], cur[2])
            root.add_child(new_node)
            mat.pop(0)
            make_tree(mat, root, new_node, lengthList)

        # add as child of previously added node
        elif lengthList < len(cur[0]):
            new_node = Tree(cur[0][lengthList - 1], cur[1], cur[2])
            previous_node.add_child(new_node)
            mat.pop(0)
            make_tree(mat, previous_node, new_node, lengthList + 1)

        # go one step up
        elif lengthList > len(cur[0]):
            make_tree(mat, root.parent,
                      previous_node, lengthList - 1)

    else:
        return


def flatten(ls):

    """To flatten a list without losing non-flat elements"""
    # the most god-awful imperative implementation ever

    ls_new = []

    for i in ls:
        if isinstance(i, list):
            for j in i:
                ls_new.append(j)
        else:
            ls_new.append(i)

    return ls_new


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

    for i in range(10):
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
    root = Tree(0, [], "")
    make_tree(matrix, root, root, 0)

    # return statement
    return root


def return_text_by_page(title, page_number):

    """Takes a particular page of the PDF file and
    returns text on that particular page"""

    # creating a pdf file object
    pdfFileObj = open(title, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    print(pdfReader.numPages)

    # creating a page object
    pageObj = pdfReader.getPage(page_number)

    # extracting text from page
    text = pageObj.extractText()

    # closing the pdf file object
    pdfFileObj.close()

    # return statement
    return text


""" Note: we parse the pdf file page-by-page, and at no
point is the entire content of the file in memory. Thus, the
maximum file size this program can handle only depends on
the system restrictions on the size of a .txt file,
and not on program memory restrictions"""


def return_document(title):

    """ to write all the text of the pdf to an
    external content.txt file,
    that does not get created within the git repository
    to account for cases where the file contains
    proprietary information"""

    # creating a pdf file object
    pdfFileObj = open(title, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # get number of pages in pdf file
    numPages = pdfReader.numPages

    # creating the file and then closing it
    f = open('content.txt', "w+")
    f.close()

    # TODO: check whether appending to an open file
    # writes to a memory buffer or file itself?
    # will matter for system memory vs. program memory
    # for large pdf files
    with open('../content.txt', 'a+') as f:

        for page_number in range(1, numPages):

            # creating a page object
            pageObj = pdfReader.getPage(page_number)

            # extracting text from page
            text = pageObj.extractText()

            # write text to file
            f.write(unicodedata.normalize('NFKD', text)
                    .encode('ascii', 'ignore'))

    # closing the pdf file object
    pdfFileObj.close()

    # program finished statement
    print("Contents of " + title + " written to ../content.txt")


def return_body(title):

    """Takes a particular heading of the PDF file and
    returns text belonging under that particular heading"""

    with open(title, 'r+') as f:

        soup = BeautifulSoup(f, 'html.parser')

        body_text = soup.body

        with open("temp/text.txt", "w+") as f2:
            f2.write(str(body_text))


# __main__

"""
if len(sys.argv) < 3:

    print "Usage:"
    print "python parse_a_pdf.py ",
    print "<path to pdf file> ",
    print "<titles/page/text> <page number?> "

else:
    title = sys.argv[1]

    if sys.argv[2] == "titles":
        print Tree.display(return_title_graph(title))

    elif sys.argv[2] == "page":
        print return_text_by_page(title, int(sys.argv[3]))

    elif sys.argv[2] == "text":
        print return_body(title)

    else:
        print "Usage:"
        print "python parse_a_pdf.py ",
        print "<path to pdf file> ",
        print "<titles/page/text> <page number?> "
"""