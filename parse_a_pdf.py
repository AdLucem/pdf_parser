"""Python module to parse a pdf and return the set of titles and
the text under each title, in JSON format"""


# importing required modules
import PyPDF2
import sys

class Tree:

    """Class to implement a title tree"""
    # int, list
    def __init__(self, nodeNum, nodeKey):

        self.id = nodeNum
        self.key = nodeKey
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

# functions


def make_tree(mat, root, previous_node, lengthList):

    if mat != []:

        cur = mat[0]

        # add on current level
        if lengthList == len(cur[0]):
            new_node = Tree(cur[0][lengthList - 1], cur[1])
            root.add_child(new_node)
            mat.pop(0)
            make_tree(mat, root, new_node, lengthList)

        # add as child of previously added node
        elif lengthList < len(cur[0]):
            new_node = Tree(cur[0][lengthList - 1], cur[1])
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


def return_title_graph(reader_object) :

    """Creating a graph of PDF titles
    and returning root node of the 
    graph"""

    outlines = pdfReader.getOutlines()

    for i in range(10):
        outlines = flatten(outlines)

    matrix = []

    # making a matrix of titles/serial numbers
    for dest in outlines:
        row = []
        title_split = dest.title.split(" ")
        row.append(map(lambda x: int(x), title_split[0].split(".")))
        title_split.pop(0)
        row.append(title_split)
        matrix.append(row)

    # making a tree out of above matrix
    root = Tree(0, [])
    make_tree(matrix, root, root, 0)

    #return statement
    return root

# __main__

title = sys.argv[1]

# creating a pdf file object
pdfFileObj = open(title, 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
# print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(3)

outlines = pdfReader.getOutlines()

for i in range(10):
    outlines = flatten(outlines)

# print(outlines)

# extracting text from page
# print(pageObj.extractText())

matrix = []

# making a matrix of titles/serial numbers
for dest in outlines:
    row = []
    title_split = dest.title.split(" ")
    row.append(map(lambda x: int(x), title_split[0].split(".")))
    title_split.pop(0)
    row.append(title_split)
    matrix.append(row)

# test print
# print(matrix)

# making a tree out of above matrix
root = Tree(0, [])
make_tree(matrix, root, root, 0)

# manually removing stopwords from each node
Tree.manual_edit(root)

# test print above matrix
# for element in matrix:
#   print element[0]," --- ",
#   print element[1]

# making a tree out of above matrix

# closing the pdf file object
pdfFileObj.close()
