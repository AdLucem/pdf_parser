"""Takes the 'cleaned' text file returned by the cleaner function (cleaners.py)
and returns:
(1) A nested file system of documents, each file being a single heading +
content in file + children of file + parent heading of file
(2) An index of headings and filepaths representing the file system"""


import unicodedata
from cleaners import clean
from utility_functions import get_titles

# ======================== FUNCTIONS ===============================


def get_text_under_title(content_file, title, next_title, pointer):

    """ Takes a title and the title after it
    and gets the text between the two"""

    sno_normal = title[0].decode('utf-8')
    next_sno_normal = next_title[0].encode('utf-8')

    title_normal = title[2].decode('utf-8')
    next_title_normal = next_title[2].decode('utf-8')

    with open(content_file, 'r+') as f:

        try:

            f.seek(pointer)

            line = f.readline().decode('utf-8')

            while not ((sno_normal in line) and (title_normal in line)):
                line = f.readline().decode('utf-8')

            print(line)
            f.seek(len(line)-1, 1)

            pointer_start = f.tell()

            if next_title_normal == 'Login procedure'.decode('utf-8'):
                print(f.readline() + "..........")

            print("Indexing text under: " + sno_normal + " " + title_normal)
            print("Indexing text before: " + next_sno_normal + " " + next_title_normal)

            while not ((next_sno_normal
                        in line) and (next_title_normal
                                      in line)):
                line = f.readline().decode('utf-8')

            f.seek(-len(line), 1)

            pointer_end = f.tell()

            # now, read the damned text
            f.seek(pointer_start)
            text = f.read(pointer_end - pointer_start)

        except EOFError:
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

    text_vs_title = []

    # hopefully these garbage strings are nowhere in the file
    title_list.append(('-1343#$%^7', ['-1$@#$%#$@@9]'], '-102342345*&$#29'))

    pointer = 0

    for index in range(0, len(title_list) - 1):

        # get the title
        title = title_list[index]

        text, pointer = get_text_under_title(content_file,
                                             title,
                                             title_list[index + 1],
                                             pointer)

        text_vs_title.append((title, text))

    return text_vs_title


def process(file_pdf, file_html):

    """Driver function to process all the data in <filename>
    and return a JSON object of text indexed by title"""

    print("Beginning processing...")

    stripped_file = clean(file_html)

    print("HTML file cleaned...")

    ls = get_titles(file_pdf)

    print("Titles fetched...")

    text_indexed_by_title = get_text_by_titles(stripped_file, ls)

    print("Text indexed by title...")

    return text_indexed_by_title
