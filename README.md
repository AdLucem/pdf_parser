# pdf_parser
A library to convert a single PDF file to a set of indexed, searchable and processable documents.

Indexes content by headings.

# Use Cases and Assumptions

- This is meant to run on technical, structured documents, like, say, user manuals. 
- We assume the pdf file has an associated table of contents, that is extracted using py2pdf.

## Usage:

```bash
./run.sh <path to pdf file>
```

## TODO

- Provision for multiple files/related files. (A little difficult to do right now because I don't have a working example of the kind of connected and multiple-document documentation I need.)
