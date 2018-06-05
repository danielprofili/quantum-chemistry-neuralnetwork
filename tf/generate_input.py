# Generate the input vector from the input file
import numpy
import argparse
import re

# handle input argument - the input file path
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="path to the input file")
parser.parse_args()

# set up regex parsing object for parsing the molecule name (TFSI_###_###)
reg = re.compile('TFSI_[0-9]{1,3}_[0-9]{1,3}')

