"""Given a file of title-lines and the html-body version of the document,
we split the document according to paragraphs assigned to titles"""

import re
import json
import sys


def grab_text_after_title(title_body, line, line_after):

    with open(title_body, 'r+') as f:

        text = f.read()

        text += "$^$"

        start = text.find(line)
        end = start + len(line)

        start_after = text.find(line_after)

        return text[end: start_after]


def grab_text_by_titles(title_body, title_headings):

    with open(title_headings, 'r+') as f:

        title_list = f.readlines()

        text_vs_title = []

        for index in range(0, len(title_list) - 1):

            try:

                title = title_list[index]

                text_vs_title.append((title,
                                      grab_text_after_title(title_body,
                                                            title,
                                                            title_list[index +
                                                                       1])))
            except IndexError:

                title = title_list[len(title_list) - 1]
                title_after = "$^$"
                text_vs_title.append((title,
                                      grab_text_after_title(title_body,
                                                            title,
                                                            title_after)))

        return text_vs_title


def strip_footers(data):

    footer = "USE OR DISCLOSURE OF DATA CONTAINED ON THIS PAGE IS SUBJECT TO\nTHE RESTRICTION ON SHEET iv OF THIS DOCUMENT.\n\n\n"

    data_new = []

    for i in data:

        d = {}
        k = i.keys()

        d[re.sub(footer, '', k[0])] = re.sub(footer, '', i[k[0]])

        data_new.append(d)

    return data_new


def strip_page_numbers(data):

    page_re = '[0-9]+\n'

    data_new = []

    for i in data:

        k = i.keys()

        if not re.match(page_re, k[0]):
            data_new.append(i)

    return data_new


def delete_figure_pointers(data):

    figure_re = 'Figure [0-9.-]+'

    data_new = []

    for index, i in enumerate(data):

        k = i.keys()[0]

        if not re.search(figure_re, k):
            data_new.append(i)

        else:

            k_prev = data_new[len(data_new) - 1].keys()
            k_prev = k_prev[0]

            # erase current dict and integrate it with previous paragraph
            # nvm, this is the shittiest line of code i've ever written
            data_new[len(data_new) - 1][k_prev] += k
            data_new[len(data_new) - 1][k_prev] += i[k]

    return data_new


def integrate_bullet_points(data):
    # fill in this function later, use the data as is for now
    return data


# I know the footers, page numbers and everything will be different
# on different documents
# modularity schmodudularity
def clean(data):

    """To clean the messy JSON data"""

    data = strip_footers(data)
    data = strip_page_numbers(data)
    data = delete_figure_pointers(data)
    data = integrate_bullet_points(data)

    return data


# __main__


text_title_list = grab_text_by_titles('temp/text.txt',
                                      'temp/lines_with_titles.txt')

obj = []

for i in text_title_list:
    d = {}
    d[re.sub('[<].*?[>]', ' ', i[0])] = re.sub('[<].*?[>]', ' ', i[1])
    obj.append(d)

obj = clean(obj)

json_obj = json.dumps(obj)

with open(sys.argv[1], 'w+') as f:

    f.write(json_obj)


print "JSON representation of file indexed by",
print " title is written to ../content.json.",
print " Happy parsing!"
