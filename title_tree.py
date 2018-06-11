"""A class to build and display a tree of text titles
from the table of contents of a pdf"""


class Tree:

    """Class representing the title tree."""

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
