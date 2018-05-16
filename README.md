# pdf_parser
A library to parse a PDF to certain text-processing-amenable formats.

##Usage:

(1) Convert the PDF you want to process to HTML. There are lots of online libraries for this, use one.

(2) The regex to identify heading-lines (identifies any and all headings, regardless of hierarchy) is on line 16 of `run.sh`, in the statement `grep -E '[>][1-9][.]?([1-9][.]){0,6}[1-9]?'`. Replace it with your own regex that identifies headings


(3) Within the pdf-parser directory, run this:

```bash
./run.sh <path_to_html_version_of_pdf>
```
