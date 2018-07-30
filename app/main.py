"""Main Function :
   Convert the pdf file into a title-indexed set of documents"""

from pdf_to_text import pdf_to_text
from clean_text import clean
from index_by_title import index_text_by_title
import sys


def pipeline():
    """Function to process pdf and return a database
    of searchable documents"""

    if len(sys.argv) != 3:
        print("""Usage:
                    ./run.sh <path to pdf file> <lines_to_be_removed>""")
    else:
        pdf_file = sys.argv[1]
        lines_to_remove = sys.argv[2]

        text_file = pdf_to_text(pdf_file)
        #cleaned_file = clean(text_file, pdf_file, lines_to_remove)
        #index_root = index_text_by_title(cleaned_file, pdf_file)
        return text_file


# driver function for the command line implementation
if __name__ == "__main__":

    pipeline()
