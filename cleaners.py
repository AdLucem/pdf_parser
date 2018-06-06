"""Cleans all the tags, images and tables off the HTML
document and normalises any elements that need to be converted
from HTML to a more parsable format"""


import os
from parse_a_pdf import return_title_graph, Tree, flatten
import re


# =============================== FUNCTIONS =============================


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


"""
def normalise_images(filename):

    Preserve images as HTML <img> tags
    referenced by page number
    and remove from main document

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
"""


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

                if (not
                    start_stripping) and ('<TABLE'
                                          in text) and ('class="t0"'
                                                        in text):
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
    ls = flatten(ls)
    return ls


def remove_tags(filename):

    """Remove all tags from the html file"""

    f = open('../cleaned_file.txt', 'w+')
    f.close()

    with open('../cleaned_file.txt', 'a+') as clean:
        with open(filename, 'r+') as dirty:

            size = os.path.getsize(os.path.abspath(filename))
            pointer = 0

            while pointer < size:
                line = dirty.readline()
                cleaned_line = re.sub('[<].+?[>]', "", line)
                clean.write(cleaned_line)
                pointer = dirty.tell()

    return '../cleaned_file.txt'


def clean(filename):

    print("Cleaning the messy HTMLized file...")

    """To strip extraneous data- i.e
    (1) Header and formatting
    (2) Table of contents
    from html file"""

    strip_header_data(filename)
    print("Removed all header and styling data...")

    needed_to_strip = strip_table_of_contents('../stripped_content.html', 2)

    iter = 3
    while needed_to_strip:
        filename = '../stripped_content_' + str(iter - 1) + '.html'
        needed_to_strip = strip_table_of_contents(filename, iter)
        iter += 1
    print("Removed table of contents...")

    clean = remove_tags(filename)
    print("Tags removed...")

    print("Cleaning done! Cleaned file: " + clean)
    return clean
