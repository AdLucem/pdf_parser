"""Main Function :
   Convert the pdf file into a title-indexed set of documents"""

from documentify import process
import sys


# driver function
if __name__ == "__main__":

    # pdf_file = raw_input("Enter filename of pdf file.\n")

    if len(sys.argv) != 2:
        print("""Usage:
                    ./run.sh <path to pdf file>""")
    else:
        process(sys.argv[1])
