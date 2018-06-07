from get_coords import get_coords


# get_coords: parse the pairwise distances between each atom
# returns a tuple containing (1) an array of the atom pair tuples and (2) an 
# array of the pairwise distances

def get_coords(xyz):
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
            tup_list = tup_list + tup
            dist_list = dist_list + dist

    return (tup_list, dist_list)
# begin the main method

# handle input argument - the input file path
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="path to the input file")
args = parser.parse_args()


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


        
# close the file
f.close()
