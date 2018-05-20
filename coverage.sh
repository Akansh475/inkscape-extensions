
export MODULES='inkex'

python3-coverage run --source $MODULES setup.py test &> /dev/null
#python2.7-coverage run -a --source $MODULES setup.py test &> /dev/null
python3-coverage report -m

