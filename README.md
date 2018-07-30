# pdf_parser
A library to convert a single PDF file to a set of indexed, searchable and processable documents.

Indexes content by headings.

# Use Cases and Assumptions

- This is meant to run on documents with a specific kind of structure, like, say, user manuals or research papers. 
- We assume the pdf file has an associated table of contents, that is extracted using py2pdf.

## Setup

To set up the environment and dependencies needed:

(1) Set up a virtualenv for dependencies (this is recommended to prevent clashing dependencies/versions). From within the `pdf-parser` directory:

```bash
virtualenv --python=/usr/bin/python2.7 venv
source venv/bin/activate
```

(2) Install dependencies using pip:

```bash
pip install -r requirements.txt
```

(3) Install nltk resources. From within the python interpreter/shell:

```python 
>>> import nltk
>>> nltk.download('punkt')
```

## Usage:

- `lines_to_be_removed` :: path to a text file containing any lines (such as headers, footers, etc) that are to be removed from the pdf file while cleaning it. The file should be a list of strings, each string being a line, each string on a separate line.

```bash
./run.sh <path to pdf file> <lines_to_be_removed>
```

## TODO

- Provision for multiple files/related files. (A little difficult to do right now because I don't have a working example of the kind of connected and multiple-document documentation I need.)
