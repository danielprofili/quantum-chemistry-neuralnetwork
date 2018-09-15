import numpy as np
import argparse
import re
import sys

# get_dists: get an array of the pairwise distances from the atoms
#   returns a N by N array (where N is the number of atoms) such that arr[i][j]
#   contains the distance (in angstroms) between atom_i and atom_j

def get_dists(xyz):
    if len(xyz) == 0:
        return [], []

    # get the xyz coords from the .xyz block
    nums = [float(s) for s in re.findall('-?\d\.\d*', xyz)]
    # the elements being used
    elems = [s for s in re.findall('[A-Z]', xyz)]
    pos = [[nums[x], nums[x+1], nums[x+2]] for x in range(0, len(nums), 3)]
    pos_np = np.array(pos)
    #tup_list = []
    #dist_list = []
    dists = np.zeros((len(elems), len(elems)))

    # find the pairwise distances (angstroms) (15 atoms choose 2 = 105)
    for i in range(0, len(pos)):
        for p in range(0, len(pos)):
            pos1 = np.array(pos[i])
            pos2 = np.array(pos[p])
            dist = np.linalg.norm(pos1-pos2) 
            # create a tuple matching the first element to the second element
            #elems_tup = (elems[i] + str(i+1),elems[p] + str(p+1))

            # better - create a 15x15 array with the distances
            dists[i][p] = dist 
            # create a tuple of the elements and the distances
            #tup_list = tup_list + elems_tup
            #tup_list.append(elems_tup)
            #dist_list = dist_list + dist
            #dist_list.append(dist)

    #return (tup_list, dist_list)
    # DEBUG
    #print(dists)
    #input("DEBUG")
    return dists, elems

# get_atom_names: get the non-unique atoms from an input qc file
def get_atom_names(inputfile):
    atom_names = []
    with open(inputfile) as f:
        line = f.readline()
        while line != '' and 'gzmat' not in line:
            line = f.readline()
        
        line = f.readline()
        if line != '':
            while line != '' and '====' not in line:
                #print(line)
                #input('pause')
                if line != '\n':
                    atom_names.append(line[0])

                line = f.readline()

    return atom_names

# begin the main method
def parse_input(inputfile):
    # handle input argument - the input file path
    # parser = argparse.ArgumentParser()
    # parser.add_argument("inputfile", help="path to the input file")
    # args = parser.parse_args()
    
    # empty list that will eventually contain 36000 perturbations' worth of 
    # tuples containing a list of all 15 atoms in order, pairwise distances,
    # and charges for each atom in order
    dist_list = []
    chg_list = []
    atom_names = get_atom_names(inputfile)
    dist_array = np.zeros((len(atom_names), len(atom_names), 1))
    charge_array = np.zeros((len(atom_names), 1));
    # set up regex parsing object for parsing the molecule name (TFSI_###_###)
    reg = re.compile('TFSI_[0-9]{1,3}_[0-9]{1,3}\.gzmat')
    #f = open(inputfile)
    #line = f.readline() 
    with open(inputfile) as f:
        line = f.readline()    
        while line != '':
            while (not (reg.match(line) or line == '')):
                # Locate the next location of xyz data
                # (i.e. where there's a TFSI_XX_XX.gzmat)
                line = f.readline()

            # now at the line containing the xyz
            line = f.readline()
            xyz = ''
            while '==================' not in line and line != '':
                xyz += line
                line = f.readline()
            
            # DEBUG
            #if "TFSI_90_99" in atom_name:
            #    print(xyz)
            #    input()

            # now have the xyz block
            dists, atoms = get_dists(xyz)
            #print(atoms)
            #print(dists)
            #print(len(dists[0]))
            #print(len(dists))
            #input()
            while "Begin charges" not in line and line != '':
                line = f.readline()

            line = f.readline()
            # next line is the first charge
            line = f.readline()
            charges = [] 
            while '==================' not in line and line != '':
                chg = re.findall('-?\d.\d*', line)
                if len(chg) > 0:
                    charges.append(float(chg[0]))
                line = f.readline()
            
            # create the big tuple containing all data for this perturbation
            #big_tuple = (atoms, dists, charges)
            #dist_list.append(big_tuple)

            # create list of all pairwise distance arrays
            # _temp arrays made so 3d arrays can be concatenated
            if len(dists) > 0:
                #dist_list.append(dists)
                dists_temp = np.zeros((len(atom_names), len(atom_names), 1))
                dists_temp[:,:,0] = dists
                #print(dist_array.shape)
                #print(dists.shape)
                dist_array = np.append(dist_array, dists_temp, 2)


            if len(charges) > 0:
                charges_temp = np.zeros((len(atom_names), 1))
                charges_temp[:,0] = charges
                charge_array = np.append(charge_array, charges_temp, 1)

            # now should go to the next atom
            # DEBUG:
            #print('atom ' + atom_name + ' done')
            #print(line)
            #if line == '':
            #    raw_input()

        # reached end of file
    
    # convert lists into 3d arrays
    #dist_array = np.zeros([len(dist_list[0]), len(dist_list[0]), len(dist_list)])
    #charge_array = np.zeros([len(chg_list[0]), len(chg_list[0]), len(chg_list)])
    #for i in range(0, len(dist_list)):
    #    print(dist_list[i])
    #    print(type(dist_list[i]))
    #    print(dist_list[i].shape)
    #    input('pause')
    #    dist_array[:][:][i] = dist_list[i]  
    #    charge_array[:][:][i] = chg_list[i] 




    # done reading the file
    #return dist_list, chg_list 
    #print(dist_array.shape)
    #print(dist_array.shape)
    #input("debug")
    return atom_names, dist_array, charge_array

# for debugging
#parse_input(sys.argv[1])
