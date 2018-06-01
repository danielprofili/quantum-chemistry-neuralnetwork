# make input files from xyz
# 1 March 2018

from random import *
import sys
import copy
import os

# get parameters from a file into a dictionary
def write_input_file(filename, filename2, xyz_file):
    f = open(filename) # template file
    f2 = open(filename2, 'w') # filename of new input file
    f_xyz = open(xyz_file) # filename of xyz file to get data from
    line = ''
    front_matter = ''
    print('reading from xyz file: ' + xyz_file)
    print('writing to input file: ' + filename2)
    while ('molecule' not in line):
        line = f.readline()
        front_matter += line

    # next line is the "molecule TFSI" line 
    #front_matter += f.readline()
    f2.write(front_matter) # write the first couple lines to the new file
    # raw_input()
    # print(front_matter)
    # current line now contains the first line in the xyz data
 
    xyz_line = f_xyz.readline()
    while 'gzmat' not in xyz_line:
        xyz_line = f_xyz.readline()
        print(xyz_line)
        # raw_input()

    xyz_line = f_xyz.readline()

    while len(xyz_line) > 0:
        f2.write(xyz_line)
        xyz_line = f_xyz.readline()
    
    # done transferring data from xyz file to input file
    # now get the rest of the stuff from the template
    
    while '-1' not in line:
        line = f.readline()

    while len(line) > 0:
        f2.write(line)
        line = f.readline()
    
    
    f.close()
    f2.close()
    f_xyz.close()
    print('done with write_input_file')
    
# end write_input_file()

# begin the main script
print('begin main function')
for fn in os.listdir('.'):
    if os.path.isfile(fn) and ('.xyz' in fn) and not ('.inp' in fn):
        # print(fn)
        if 'TFSI_temp.inp' not in fn:
            write_input_file('TFSI_temp', fn[:len(fn)-4] + '.inp', fn)
            # pause() # not actually a method but it stops the program
            print('Wrote ' + fn + '.inp\n')


