import numpy as np
import argparse
import re
import sys

# get_dists: parse the pairwise distances between each atom
# returns a tuple containing (1) an array of the atom pair tuples and (2) an 
# array of the pairwise distances

def get_dists(xyz):
    # get the xyz coords from the .xyz block
    nums = [float(s) for s in re.findall('-?\d\.\d*', xyz)]
    elems = [s for s in re.findall('[A-Z]', xyz)]

    # arrange them into a triplet for each molecule
    pos = [[nums[x], nums[x+1], nums[x+2]] for x in range(0, len(nums), 3)]
    tup_list = []
    dist_list = []

    # find the pairwise distances (angstroms) (15 atoms choose 2 = 105)
    for i in range(0, len(pos)):
        for p in range(i+1, len(pos)):
            pos1 = np.array(pos[i])
            pos2 = np.array(pos[p])
            dist = np.linalg.norm(pos1-pos2) 
            # create a tuple matching the first element to the second element
            elems_tup = (elems[i] + str(i+1),elems[p] + str(p+1))
            
            # create a tuple of the elements and the distances
            #tup_list = tup_list + elems_tup
            tup_list.append(elems_tup)
            #dist_list = dist_list + dist
            dist_list.append(dist)

    return (tup_list, dist_list)


# begin the main method
def parse_input(inputfile):
    # handle input argument - the input file path
    # parser = argparse.ArgumentParser()
    # parser.add_argument("inputfile", help="path to the input file")
    # args = parser.parse_args()
    
    # empty list that will eventually contain 36000 perturbations' worth of 
    # tuples containing a list of all 15 atoms in order, pairwise distances,
    # and charges for each atom in order
    big_list = []
    # set up regex parsing object for parsing the molecule name (TFSI_###_###)
    reg = re.compile('TFSI_[0-9]{1,3}_[0-9]{1,3}\.gzmat')
    f = open(inputfile)
    line = f.readline() 
    while line != '':
        while (not reg.match(line) and f != ''):
            line = f.readline()
        atom_name = line
        # now at the line containing the xyz
        line = f.readline()
        xyz = ''
        while '==================' not in line:
            xyz += line
            line = f.readline()
        
        # now have the xyz block
        atoms, dists = get_dists(xyz)
        
        while "Begin charges" not in line:
            line = f.readline()
        line = f.readline()
        # next line is the first charge
        line = f.readline()
        charges = [] 
        while '==================' not in line:
            chg = re.findall('-?\d.\d*', line)
            if len(chg) > 0:
                charges.append(float(chg[0]))
            line = f.readline()
        
        # create the big tuple containing all data for this perturbation
        big_tuple = (atoms, dists, charges)
        big_list.append(big_tuple)

        # now should go to the next atom
        # DEBUG:
        print('atom ' + atom_name + ' done')
        print(line)
        if line == '':
            raw_input()


    # close the file
    f.close()
    return big_list

# for debugging
parse_input(sys.argv[1])
