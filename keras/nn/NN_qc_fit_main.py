import sys
import copy
from keras.models import Model, Sequential, load_model
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
import sys

inputfile = sys.argv[1]

# read input data, output as numpy arrays
(aname, rij, charges ) = gen.parse_input( inputfile )

# need list (over atoms) of array (over data points) for charges
charge_list=[ charges[i,1:] for i in range(charges.shape[0]) ]

# FOR TESTING
rij = rij[:,:,1:]

# load the Neural network force field definitions
NNff = NNforce_field( 'FF3', aname )

# construct symmetry functions for NN input
sym_input = routines.construct_symmetry_input( NNff , rij , aname )

if len(sys.argv) == 2:
    # construct NN model
    model = construct_NN_Model( sym_input, NNff, aname )

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    print( "fitting Neural network to charge data...")

    #history=model.fit( sym_input , charges, batch_size=20, epochs=5000, validation_split=0.1 )
    history=model.fit( sym_input , charge_list, batch_size=20, epochs=5000, validation_split=0.1)

    print( "done fitting Neural network" )

    print( "summary" )

    model.summary()
    model.save(inputfile[:-2] + "_model")

    y = model.predict_on_batch( sym_input )
    model_path = "model_" + inputfile[-4:]
    print("Saving model to " + model_path)
    model.save(model_path)

else:
    model = load_model(sys.argv[2])
    y = model.predict_on_batch( sym_input)

# y is a 15xN array with the results for each atom
# charge_list is a 15xN array with the QM charges
#print(y[0].shape)
#print(y[0])
#input("y shape continue?")

print(y[0])
print(charge_list)
# print(aname)
# 
# input()

# generate the plots
for i in range(len(aname)):
    q_qm = charge_list[i]
    q_nn = y[i]

    #new_list = []
    #new_qm_list = []
    #for j in range(len(q_nn)):
    #    new_list = new_list + [q_nn[j][0]]
    #    new_qm_list = new_qm_list + [q_qm[j]]

    nn_plot.plot_atom("test/" + aname[i] + str(i), q_nn, q_qm)

# print("QM total charge: " + str(np.sum(y[:, 0])))
# print("NN total charge: " + str(np.sum(y[:, 1])))



