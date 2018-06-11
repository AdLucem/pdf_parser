
# setup

#if [ ! -d "venv" ]; then
#	virtualenv --python=/usr/bin/python2.7 venv
#fi

#source venv/bin/activate
#pip install -r requirements.txt


# processing

python convert_pdf.py $1

# teardown

# rm -r temp
# deactivate
