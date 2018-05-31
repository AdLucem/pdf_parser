"""Takes the html conversion of the given pdf file and
returns the original doc, indexed by heading"""


import os
import sys
from parse_a_pdf import return_title_graph, Tree, flatten
import unicodedata
import re
import json


def strip_header_data(filename):
    """ Remove all data between head tags
    i.e: all html formatting data"""

    start = 0
    num_bytes = 1000
    # *finger guns* ayyyyyy
    start_stripping = False

    # creating a file to append the stripped data to
    f = open('../stripped_content.html', 'w+')
    f.close()

    with open('../stripped_content.html', 'a+') as f_str:
        with open(filename, 'r+') as f:

            # get size of file
            file_size = os.path.getsize(os.path.abspath(filename))

            while start < file_size:

                text = f.read(num_bytes)
                start += num_bytes

                if not start_stripping and '<HEAD>' in text:
                    start_stripping = True

                if start_stripping:

                    if '</HEAD>' in text:

                        lines = text.split('\n')
                        for index, line in enumerate(lines):
                            if '</HEAD>' in line:
                                for i in lines[index + 1:]:
                                    f_str.write(i + '\n')
                                break

                        start_stripping = False

                elif not start_stripping:
                    f_str.write(text)


def normalise_images(filename):

    """Preserve images as HTML <img> tags
    referenced by page number
    and remove from main document"""

    page_no = 0
    images = []

    with open(filename, 'r+') as f:

        # get size of file
        file_size = os.path.getsize(os.path.abspath(filename))

        while pointer < file_size:

            line = f.readline()
            start += num_bytes

            if_page = re.search("[<]DIV\sid=\"page[_]<page_number>*\"[>]",
                                line)
            if if_page:
                page_no = int(if_page.group('page_number'))
                print(page_no)

            if re.search('[<]IMG', line):
                is_image = True
                img = (page_no, line)
                images.append(img)

    # write images as json object to file
    data = []
    for index, img in images:
        d = {}
        d['id'] = index
        d['page'] = img[0]
        d['image_tag'] = img[1]
        data.append(d)

    with open('../images.json', 'w+') as f:
        f.write(json.dumps(data))


def strip_table_of_contents(filename, iter):
    """Remove the table of contents, assumed here to be the
    first table"""

    start = 0
    num_bytes = 1000
    # *finger guns* ayyyyyy
    start_stripping = False
    needed_to_strip = False

    # creating a file to append the stripped data to
    f = open('../stripped_content_' + str(iter) + '.html', 'w+')
    f.close()

    with open('../stripped_content_' + str(iter) + '.html', 'a+') as f_str:
        with open(filename, 'r+') as f:

            # get size of file
            file_size = os.path.getsize(os.path.abspath(filename))

            while start < file_size:

                text = f.read(num_bytes)
                start += num_bytes

                if (not start_stripping) and ('<TABLE' in text) and ('class="t0"' in text):
                    start_stripping = True
                    needed_to_strip = True

                if start_stripping:

                    if '</TABLE>' in text:

                        lines = text.split('\n')
                        for index, line in enumerate(lines):
                            if '</TABLE>' in line:
                                for i in lines[index + 1:]:
                                    f_str.write(i + '\n')
                                break

                        start_stripping = False

                elif not start_stripping:
                    f_str.write(text)

    return needed_to_strip


def get_titles(filename):

    """Fetch a list of titles in the format:
    (<serial number>, <list of tokens in title>, <title without serial number>)
    from the original pdf file"""

    graph = return_title_graph(filename)
    ls = Tree.tree_to_list(graph)
    for i in range(10):
        ls = flatten(ls)
    return ls


def strip_extraneous_data(filename):

    """To strip extraneous data- i.e
    (1) Header and formatting
    (2) Table of contents
    from html file"""

    strip_header_data(filename)

    needed_to_strip = strip_table_of_contents('../stripped_content.html', 2)
    iter = 3
    while needed_to_strip:
        filename = '../stripped_content_' + str(iter - 1) + '.html'
        needed_to_strip = strip_table_of_contents(filename, iter)
        iter += 1
    return filename


def get_text_under_title(content_file, title, next_title, pointer):

    """ Takes a title and the title after it
    and gets the text between the two"""

    title_normal = unicodedata.normalize('NFKD', title[2]).encode('ascii', 'ignore')
    next_title_normal = unicodedata.normalize('NFKD', next_title[2]).encode('ascii', 'ignore')

    with open(content_file, 'r+') as f:

        try:

            f.seek(pointer)

            line = f.readline()

            while (title[0] not in line) and (title_normal not in line):
                line = f.readline()

            f.seek(len(line), 1)

            pointer_start = f.tell()

            print("Indexing text before: " + next_title_normal)

            while (next_title[0] not in line) and (next_title_normal not in line):
                line = f.readline()
                #f.seek(len(line), 1)
                #print(f.tell())

            f.seek(-len(line), 1)

            pointer_end = f.tell()

            # now, read the damned text
            f.seek(pointer_start)
            text = f.read(pointer_end - pointer_start)

        except EOFError:
            f.seek(pointer_start)
            text = f.read()
            pointer_end = '-100'

    print("Indexed text under: " + title_normal)
    return text, pointer_end


def get_text_by_titles(content_file, title_list):

    text_vs_title = []

    # hopefully these garbage strings is nowhere in the file
    title_list.append(('-1000000007', ['-1000000009]'], '-1000000029'))

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

    stripped_file = strip_extraneous_data(file_html)

    print("HTML file processed...")

    ls = get_titles(file_pdf)

    print("Titles fetched...")

    text_indexed_by_title = get_text_by_titles(stripped_file, ls)

    print("Text indexed by title...")

    return text_indexed_by_title


# __main__

print(process(sys.argv[1], sys.argv[2]))
