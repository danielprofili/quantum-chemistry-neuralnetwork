# Generate the input vector from the input file
# 5 June 2018
import numpy
import argparse
import re
import numpy as np

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

# get the xyz coords from the .xyz block
nums = [float(s) for s in re.findall('-?\d\.\d*', xyz)]

# arrange them into a triplet for each molecule
pos = [[nums[x], nums[x+1], nums[x+2]] for x in range(0, len(nums), 3)]

# find the pairwise distances (15 C 2 = 105)
for i in range(0, len(pos)):
    for p in range(i+1, len(pos)):
        pos1 = np.array(pos[i])
        pos2 = np.array(pos[p])
        dist = np.linalg.norm(pos1-pos2) 



# close the file
f.close()


