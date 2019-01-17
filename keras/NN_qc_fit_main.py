import sys
import copy
from keras.models import Model, Sequential
from keras.layers import Input, Lambda, Dense, Activation, concatenate, add, LocallyConnected1D
import keras.backend as K
import tensorflow as tf
import numpy as np
import routines2 as routines
import get_test_data as gt
import generate_input as gen
#from FFenergy_openMM import compute_SAPT_FF_energies
import symmetry_functions as sym
from force_field_parameters import *
from construct_NN import construct_NN_Model
import nn_plot


inputfile='input.qc'

# read input data, output as numpy arrays
(aname, rij, charges ) = gen.parse_input( inputfile )
#for i in range(len(aname)):


#print(np.histogram(charges[2]))
#input('debugging')
#print(rij.shape)
#input('shape of rij')

# need list (over atoms) of array (over data points) for charges
charge_list=[ charges[i,:] for i in range(charges.shape[0]) ]

# FOR TESTING
#rij = rij[:,:,1:3600]
#charge_list=[ charges[i,1:] for i in range(charges.shape[0]) ]
#charge_list = copy.deepcopy(charges)

#print(rij[:,:,1])
#print(rij.shape)
#input('shape of rij again')
#print(charges)
#print(charges.shape)
#input('debug')
#print(aname)


# DEBUGGING
#(xyz_sample, charges_sample) = gt.get_test_data();
#print(xyz_sample)
#print(xyz_sample.shape[2])

# compute SAPT-FF energies
#energy_SAPTFF = compute_SAPT_FF_energies( xyz , 'h2o_template.pdb', 'water_residue.xml' , 'water_sapt.xml' )

#for i in range(len(energy_SAPTFF)):
#    print( energy[i]*2.6255, energy_SAPTFF[i] )

# fit to the residual, (kJ/mol)
#energy_fit = energy * 2.6255 - np.array( energy_SAPTFF )

# load the Neural network force field definitions
NNff = NNforce_field( 'FF3', aname )

# compute displacement tensor for all data points, output as numpy array
#rij = routines.compute_displacements(xyz)

# construct symmetry functions for NN input
sym_input = routines.construct_symmetry_input( NNff , rij , aname )

#sym_input = np.array(sym_input)
#sym_input_new = []
#for i in range(len(aname)):
#    print(sym_input[i, :, :])
#    sym_input_new.append(sym_input[i, :, :]) 
#sym_input = sym_input_new

# construct NN model
model = construct_NN_Model( sym_input, NNff, aname )

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

print( "fitting Neural network to charge data...")
#print(np.array(sym_input).shape)
#print(np.array(charges).shape)
#input("DEBUG")

#history=model.fit( sym_input , charges, batch_size=20, epochs=5000, validation_split=0.1 )
history=model.fit( sym_input , charge_list, batch_size=20, epochs=50, validation_split=0.1)

print( "done fitting Neural network" )

print( "summary" )

model.summary()

y = model.predict_on_batch( sym_input )

# y is a 15xN array with the results for each atom
# charge_list is a 15xN array with the QM charges

# print(y[0])
# print(charge_list)
# print(aname)
# 
# input()

# generate the plots
for i in range(len(aname)):
    q_qm = charge_list[i]
    q_nn = y[i]
    print(q_qm)
    print()
    print(q_nn)
    input()
    nn_plot.plot_atom(aname[i] + str(i), q_nn, q_qm)


# 
# print( "QM charges     NN charges" )
# 
# for i in range(charge_list[0].shape[0]):
#     print( "data point " , i )
#     for j in range(len(charge_list)):
#         print( charge_list[j][i] ,  y[j][i][0] ) 
# 
# y = np.array(y)
# 
# print("QM total charge: " + str(np.sum(y[:, 0])))
# print("NN total charge: " + str(np.sum(y[:, 1])))


#print( "SAPT energy, NN-SAPT-FF energy ")
#for i in range(len(energy)):
#    print( energy[i]*2.6255 , energy_SAPTFF[i] + y[i][0] )


