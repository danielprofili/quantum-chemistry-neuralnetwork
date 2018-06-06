# Generate the input vector from the input file
# 5 June 2018
import numpy
import argparse
import re

# handle input argument - the input file path
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="path to the input file")
args = parser.parse_args()

def get_coords(xyz_mat):
   print("asdasd") 

# set up regex parsing object for parsing the molecule name (TFSI_###_###)
reg = re.compile('TFSI_[0-9]{1,3}_[0-9]{1,3}\.gzmat')
f = open(args.inputfile)
line = f.readline() 
while (not reg.match(line) and f != ''):
    line = f.readline()

# now at the line containing the xyz
# TODO DEBUG:
# print(line)
line = f.readline()
xyz = ''
while '==================' not in line:
    xyz += line
    line = f.readline()

# print(xyz)
#print(re.findall('-?\d\.\d*', xyz))
nums = [float(s) for s in re.findall('-?\d\.\d*', xyz)]
# print(nums)
for i in range(0, len(nums)):
    print(nums[i])
f.close()


