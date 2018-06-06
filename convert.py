"""Convert the pdf file into a title-indexed set of documents"""

from preprocess import process


if __name__ == "__main__":

    # pdf_file = raw_input("Enter filename of pdf file.\n")
    # html_file = raw_input("Enter filename of htmlised pdf file.\n")

    process("../ipms.pdf", "../ipms.html")
