"""To fetch and handle the hierarchy of titles
in the contents list of pdf file"""

from nltk import word_tokenize
import PyPDF2

# ============================ CLASSES ====================================


class Tree:

    """A class to build and display a tree of text titles
    from the table of contents of a pdf"""

    def __init__(self, bulletNum, nodeKey, originalTitle):

        """Init function. Args:
        <bullet number> :: String
        <tokenised heading> :: [String]
        <non-tokenised heading> :: String"""

        self.bullet = bulletNum
        self.key = nodeKey
        self.original = originalTitle
        self.parent = 0
        self.children = []

    def add_child(self, childNode):

        """To add a child to the given node. Args:
        <node to be added> :: Tree"""

        self.children.append(childNode)
        childNode.parent = self

    @staticmethod
    def display(root):

        """To neatly display all the tree contents in
        the order they are in the original pdf index.
        It's a basic recursive tree-display algorithm. Args:
        <root of tree> :: Tree"""

        if not root:
            return

        print root.bullet, " :: ", root.key

        if root.children == []:
            return
        else:
            for i in root.children:
                Tree.display(i)

    @staticmethod
    def tree_to_list(root):

        """Convert a tree to a flat list. A basic
        recursive tree-display algorithm. Args:
        <root of tree> :: Tree"""

        ls = []

        if not root:
            return ls

        ls.append((root.bullet, root.key, root.original))

        if root.children == []:
            return ls
        else:
            return ls + [Tree.tree_to_list(i) for i in root.children]


# ============================ MAIN FUNCTIONS ==============================


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


# ========================== UTILITY FUNCTIONS ============================


def get_flat_title_list(filename):

    """Fetch a list of titles in the format:
    (<serial number>, <list of tokens in title>, <title without serial number>)
    from the original pdf file"""

    graph = return_title_graph(filename)
    ls = Tree.tree_to_list(graph)
    ls = flatten(ls)

    ln = []

    # normalise title encoding
    for (sno, title_tokens, title) in ls:
        ln.append((nmls(sno), title_tokens, nmls(title)))

    ln.pop(0)
    return ln


def nmls(text):
    """To avoid funny encoding errors"""
    return text.encode('ascii', 'ignore')
