"""A few utility functions for parsing a pdf"""


import PyPDF2
import unicodedata
from bs4 import BeautifulSoup
from build_title_tree import Tree, return_title_graph, flatten

# ===================== FUNCTIONS ==============================


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
            f.write(unicodedata.normalize('NFKD', text))

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


def get_titles(filename):

    """Fetch a list of titles in the format:
    (<serial number>, <list of tokens in title>, <title without serial number>)
    from the original pdf file"""

    graph = return_title_graph(filename)
    ls = Tree.tree_to_list(graph)
    ls = flatten(ls)
    return ls
