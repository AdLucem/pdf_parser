"""Takes the 'cleaned' text file returned by the cleaner function (cleaners.py)
and returns:
(1) A nested file system of documents, each file being a single heading +
content in file + children of file + parent heading of file
(2) An index of headings and filepaths representing the file system"""


import subprocess
import os
import json
import re
from fuzzywuzzy import fuzz
from cleaners import clean
from utility_functions import get_titles

# ======================== FUNCTIONS ===============================


def fuzzy_match(title, line):

    """Fuzzy matching between the title and the line
    given. Returns true/false value"""

    # extract needed bits from title
    sno = title[0]
    text = title[2]

    approx_title = sno + " " + text
    match = fuzz.token_sort_ratio(approx_title, line)

    if match >= 95:
        return True
    elif match > 90:
        # check a bit more closely

        title_list = approx_title.split(' ')
        title_list = filter(lambda x: x != '', title_list)

        line_list = line.split(' ')
        line_list = filter(lambda x: x != '', line_list)

        # if the line is within one or two tokens of the title
        if (len(line_list) >=
            len(title_list) - 2) and (len(line_list) <=
                                      len(title_list)):

            flag = True
            # if the line is title_list but missing a few words
            for i in range(len(line_list)):
                submatch = fuzz.ratio(line_list[i], title_list[i])
                if submatch < 95:
                    flag = False
                    break
            if flag:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def get_text_under_title(content_file, title, next_title, pointer, fsize):

    """ Takes a title and the title after it
    and gets the text between the two"""

    with open(content_file, 'r+') as f:

        if pointer < fsize:

            f.seek(pointer)

            line = f.readline()

            while not fuzzy_match(title, line):
                line = f.readline()

            pointer_start = f.tell()

            #print("Indexing text under: " + title[0] + " " + title[2])
            #print("Indexing text before: " + next_title[0] + " " + next_title[2])

            endflag = False
            while not fuzzy_match(next_title, line):

                if re.search('[1-9][.]', line):
                    print(next_title[0] + " " + next_title[2])
                    print()

                if f.tell() < fsize:
                    line = f.readline()
                else:
                    endflag = True
                    break

            if endflag:
                f.seek(0, 2)
            else:
                f.seek(-len(line), 1)

            pointer_end = f.tell()

            # now, read the damned text
            f.seek(pointer_start)
            text = f.read(pointer_end - pointer_start)

        else:
            f.seek(pointer_start)
            text = f.read()
            pointer_end = '-100'

    return text, pointer_end


def get_text_by_titles(content_file, title_list):

    """ Takes the content file and a flat list of titles and
    associates each title with a span of text
    Args:
        <text file> :: String
        <list of titles> :: [String]"""

    # fetch size of the content file
    fsize = os.path.getsize(os.path.abspath(content_file))

    text_vs_title = []

    # hopefully these garbage strings are nowhere in the file
    title_list.append(('EOF', ['-1$@#$%#$@@9]'], '-102342345*&$#29'))

    pointer = 0

    for index in range(0, len(title_list) - 1):

        # get the title
        title = title_list[index]
        # get the title after
        next_title = title_list[index + 1]

        text, pointer = get_text_under_title(content_file,
                                             title,
                                             next_title,
                                             pointer, fsize)

        text_vs_title.append({'id': index, 'title': title, 'text': text})

    return text_vs_title


def process(file_pdf):

    """To process all the data in <filename>
    and return a JSON object of text indexed by title"""

    print("Converting pdf to text...")

    subprocess.call(['pdftotext', '-layout', '-nopgbrk', file_pdf])

    file_text = file_pdf.rstrip('pdf') + 'txt'

    print("""Cleaning text file-
            removing table of contents, page numbers, footers...""")

    stripped_file = clean(file_text)

    print("Fetching titles...")

    ls = get_titles('../' + file_pdf)

    print("Titles fetched...")

    text_indexed_by_title = get_text_by_titles(stripped_file, ls)

    print("Text indexed by title...")

    jsonfile = '../' + file_pdf.rstrip('pdf') + 'json'
    with open(jsonfile, 'w+') as f:
        jsondata = json.dumps(text_indexed_by_title)
        f.write(jsondata)

    print("Text indexed by title in JSON format in the file: " + jsonfile)
