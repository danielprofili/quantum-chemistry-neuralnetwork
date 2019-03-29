#!/usr/bin/python
# perturb parameters for TFSI
# 24 February2018

from random import *
import sys
import copy
import argparse
import os
import ntpath

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
    # print params
    f.close()
    return params, front_matter
# end get_params()


# puts parameters from params into a new .gzmat file
def put_params(filename):
    f = open(filename, 'w')
    f.write(front_matter)
    for k, v in params.iteritems():
        f.write(k + '= ' + str(v) + '\n')
    # print the d9 parameter
    # f.write('d9= ' + str(th) + '\n')
    f.close()
# end put_params()

############################################# begin main script ######################################## 
# TODO - command line args
#if len(sys.argv) > 1:
#    template_file_name = str(sys.argv[1])
#else:
#    template_file_name = 'TFSI.gzmat'

parser = argparse.ArgumentParser(description='Generate perturbations on z-matrix files in .gzmat format.')
# required argument - template file to start from
parser.add_argument('template_file', metavar='Template', help='gzmat file to perturb')

# optional args
parser.add_argument('--output-dir', dest='output_dir', help='directory in which to output', default=os.getcwd())
parser.add_argument('--count', dest='count', type=int, help='total number of perturbations', default=10000)
parser.add_argument('--reset', dest='reset', type=int, help='number of perturbations after which the state of the molecule will be reset', default=100)
parser.add_argument('--percent', dest='percent', type=float, help='how much the molecule is perturbed by each cycle', default=0.05)
parser.add_argument('--rotate', dest='rotate', nargs=3, metavar='DIHEDRAL FREQ INTERVAL', help='rotates about a specific dihedral every FREQ cycles by INTERVAL degrees')
args = parser.parse_args()

th = 0
# rotate if specified rotate option
rotate = args.rotate != None
template_file_name = args.template_file
params, front_matter = get_params(template_file_name)
    
# save the initial state for later resetting
init_params = copy.deepcopy(params)

# create output dir if it doesn't exist
if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

# begin cycling
for i in range(0, args.count):
    if i % args.reset == 0:
        params = copy.deepcopy(init_params)

    if rotate and i % int(args.rotate[1]) == 0:
        th = th + int(args.rotate[2])

    vars_list = list(params.keys())
    if rotate:
        # don't vary the axis of rotation
        var_vary = args.rotate[0]
        while var_vary == args.rotate[0]:
            vary_ind = randint(0, len(params) - 1)
            var_vary = vars_list[vary_ind]
    else:
        # anything goes
        vary_ind = randint(0, len(params) - 1)
        var_vary = vars_list[vary_ind]

    # perturb the selected variable within 10%
    var_val = params[var_vary]
    var_val *= (random() * 2 * args.percent) + (1 - args.percent) 

    # put back into param dict
    params[var_vary] = var_val

    # write new file
    base_path = ntpath.basename(template_file_name)
    base, ext = base_path.split('.')
    if rotate:
        params[args.rotate[0]] = th
        put_params(args.output_dir + '/' + base + '_' + str(th) + '_' +  str(i) + '.' + ext)
    else:
        put_params(args.output_dir + '/' + base + '_' +  str(i) + '.' + ext)

# put_params('test.gzmat', th)
#while th <= 360:
#    for i in range(0, 100):
#        vars_list = list(params.keys())
#        var_vary = 'd9'
#        while var_vary == 'd9':
#            vary_ind = randint(0, len(params) - 1)
#            var_vary = vars_list[vary_ind]
#        # print var_vary
#
#        # perturb the selected variable within 10%
#        var_val = params[var_vary]
#        var_val *= (random() * 0.2) + 0.9 
#
#        # put back into param dict
#        params[var_vary] = var_val
#
#        # write new file
#        params['d9'] = th
#        put_params(template_file_name[:4] + '_' + str(th) + '_' +  str(i) + '.gzmat')
#
#    # end for
#    th += 10
#    # reset the parameters
#    params = copy.deepcopy(init_params)

# end perturb.py
