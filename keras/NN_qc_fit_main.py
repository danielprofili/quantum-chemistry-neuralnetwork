import sys
from keras.models import Model, Sequential
from keras.layers import Input, Lambda, Dense, Activation, concatenate, add, LocallyConnected1D
import keras.backend as K
import tensorflow as tf
import numpy as np
import routines2 as routines
import generate_input as gen
from FFenergy_openMM import compute_SAPT_FF_energies
import symmetry_functions as sym
from force_field_parameters import *
from construct_NN import construct_NN_Model


inputfile='input.qc'

# read input data, output as numpy arrays
(aname, rij, charges ) = gen.parse_input( inputfile )
# coordinates read in as Bohr
#print("NN will use bohr units consistent with input coordinates")

# compute SAPT-FF energies
energy_SAPTFF = compute_SAPT_FF_energies( xyz , 'h2o_template.pdb', 'water_residue.xml' , 'water_sapt.xml' )

#for i in range(len(energy_SAPTFF)):
#    print( energy[i]*2.6255, energy_SAPTFF[i] )

# fit to the residual, (kJ/mol)
energy_fit = energy * 2.6255 - np.array( energy_SAPTFF )

# load the Neural network force field definitions
NNff = NNforce_field( 'FF3' )

# compute displacement tensor for all data points, output as numpy array
#rij = routines.compute_displacements(xyz)

# construct symmetry functions for NN input
sym_input = routines.construct_symmetry_input( NNff , rij , aname )

# construct NN model
model = construct_NN_Model( sym_input, NNff, aname )

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

print( "fitting Neural network to interaction energy data...")
history=model.fit( sym_input , energy_fit, batch_size=20, epochs=5000, validation_split=0.1 )
print( "done fitting Neural network" )
 
print( "summary" )
model.summary()

print( "predictions" )
y = model.predict_on_batch( sym_input )

print( "SAPT energy, NN-SAPT-FF energy ")
for i in range(len(energy)):
    print( energy[i]*2.6255 , energy_SAPTFF[i] + y[i][0] )



