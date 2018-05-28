# perturb parameters for TFSI
# 25 January 2018

from random import *


# get parameters from a file into a dictionary
def get_params(filename):
    f = open(filename)
    line = ''
    front_matter = ''
    params = {}
    while ('Variables:' not in line):
        # repeatedly throw away useless lines in the file
        # until the variable section is reached
        line = f.readline()
        front_matter += line

    # throw away the next line
    # front_matter += f.readline()

    # current line now contains the first variable
 
    line = f.readline()
    while len(line) > 0:
        substrs = line.split('=')
        if len(substrs) > 1:
            params[substrs[0]] = float(substrs[1])

        line = f.readline()

    # print line
    print params
    f.close()
    return params, front_matter

# puts parameters from params into a new .gzmat file
def put_params(filename):
    f = open(filename, 'w')
    f.write(front_matter)
    for k, v in params.iteritems():
        f.write(k + '= ' + str(v) + '\n')
    f.close()


# TODO - command line args
template_file_name = 'TFSI.gzmat'
th = 0
params, front_matter = get_params(template_file_name)
init_params = params

put_params('test.gzmat', params)
while th <= 360:
    for i in range(0, 100):
        vars_list = list(params.keys())
        var_vary = 'd9'
        while var_vary == 'd9':
            vary_ind = randint(0, len(params) - 1)
            var_vary = vars_list[vary_ind]
        # print var_vary

        # perturb the selected variable within 10%
        var_val = params[var_vary]
        var_val *= (random() * 0.2) + 0.9 

        # put back into param dict
        params[var_vary] = var_val

        # write new file
        put_params(template_file_name[:5] + str(i) + '.gzmat')

    th += 10
    # reset the parameters
    params = init_params
    
