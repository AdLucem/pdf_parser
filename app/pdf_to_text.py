"""Converts the pdf file to an equivalent text file-
preserving the layout and omitting pagebreaks-
using bash shell commands"""

import subprocess


def pdf_to_text(pdf_path):

    print("Converting pdf to text...")

    subprocess.call(['pdftotext', '-layout', '-nopgbrk', pdf_path])
    subprocess.call(
        ['mv', pdf_path.rstrip('pdf') + 'txt', '../searchdata.txt'])

    # return output file path
    return '../searchdata.txt'
