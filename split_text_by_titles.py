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


# __main__


text_title_list = grab_text_by_titles('temp/text.txt',
                                      'temp/lines_with_titles.txt')

d = {}

for i in text_title_list:
    d[re.sub('[<].*?[>]', '', i[0])] = re.sub('[<].*?[>]', '', i[1])

json_obj = json.dumps(d)

with open(sys.argv[1], 'w+') as f:

    f.write(json_obj)


print "JSON representation of file indexed by",
print " title is written to ../content.json.",
print " Happy parsing!"



