
# setup

if [ ! -d "venv" ]; then
	virtualenv --python=/usr/bin/python2.7 venv
fi

source venv/bin/activate
pip install -r requirements.txt


# processing

mkdir temp
python parse_a_pdf.py $1 text
sed -i 1,953d temp/text.txt
cat temp/text.txt | grep -E '[>][1-9][.]?([1-9][.]){0,6}[1-9]?' > temp/lines_with_titles.txt
python split_text_by_titles.py ../content.json


# teardown

rm -r temp
deactivate
