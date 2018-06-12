# pdf_parser
A library to convert a single PDF file to a set of indexed, searchable and processable documents.

Indexes content by headings.

# Use Cases and Assumptions

- This is meant to run on technical, structured documents, like, say, user manuals. 
- We assume the pdf file has an associated table of contents, that is extracted using py2pdf.
- natural language is a scourge upon planet earth and should be eradicated. all hail our formal-language-speaking robot overlords
- now I understand why CBSE exam evaluators dock marks for wrong formatting in our answer sheet
Seeing the documentation, I find myself wanting to dock lives for irregular formatting in the pdf.

## Usage:

```bash
./run.sh <path to pdf file>
```

## TODO

- Provision for multiple files/related files. (A little difficult to do right now because I don't have a working example of the kind of connected and multiple-document documentation I need.)
