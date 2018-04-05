
python3-coverage run --source Barcode,inkex setup.py test &> /dev/null
python2.7-coverage run -a --source Barcode,inkex setup.py test &> /dev/null
python3-coverage report -m

