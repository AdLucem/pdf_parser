"""Main Function :
   Convert the pdf file into a title-indexed set of documents"""

from documentify import process
import sys


def convert():
    """Main function"""

    if len(sys.argv) != 2:
        print("""Usage:
                    ./run.sh <path to pdf file>""")
    else:
        process(sys.argv[1])


# driver function for the command line implementation
if __name__ == "__main__":

    convert()
