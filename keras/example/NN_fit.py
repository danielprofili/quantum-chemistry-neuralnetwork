import sys
from keras.models import Model, Sequential
from keras.layers import Input, Lambda, Dense, Activation, concatenate
import keras.backend as K
import numpy as np
import routines as routines
import symmetry_functions as sym
from force_field_parameters import *

inputfile='h2o_h2o_dummy_Eint_10mh.bohr'

# read input data, output as numpy arrays 
(aname, xyz, energy ) = routines.read_sapt_data( inputfile )

# load the Neural network force field definitions
NNff = NNforce_field( 'FF1' )

# compute displacement tensor for all data points, output as numpy array
rij = routines.compute_displacements(xyz)
print(rij)
input()

# construct symmetry functions for NN input 
sym_input = routines.construct_symmetry_input( NNff , rij , aname )

#*****************************************
# call this routine if we want to compute histrograms of symmetry input
# over the dataset.  This will print histograms and exit code
#******************************************
#flag = routines.test_symmetry_input(sym_input)

# the number of unique neural networks is the number of unique elements, create
# list linking elements to unique atomtypes
(ntype, atype, atypename) = routines.create_atype_list( aname )


# now construct NN model
# for keras 2.2, the Network/Model class is found in source keras/engine/network.py
# for keras 2.1.6, there is no Model class, but the highest class is 'layer', found in keras/engine/topology.py
# the class "Dense" is the standard type of neural-network layer, found in /keras/layers/core.py


#******* hidden layers *********
# outputs the atomic energies, so output dimension (units) is Natom
# use arctan for activation function

# here we initialize a list of element specific NNs, where each NN is a 1-D layer
# we need a unique layer object for each element, for each layer.  Thus loop over layers and elements

n_layer=2
NNunique=[]
inputelement=[]

# loop over elements, each final layer returns atomic energy of size '1'
for i_type in range(ntype):
    NNelement=[]
    i_size = len(NNff.element_force_field[ atypename[i_type] ].symmetry_functions )
    for i_layer in range(n_layer):
        # if last hidden layer, output size is 1, else output size
        # is same as input size
        if i_layer == n_layer - 1:
            i_size_l = 1
        else:
            i_size_l = i_size

        # create unique NN layer object for this element and this layer, don't
        # provide input tensor, as we want to keep this abstract object to apply
        # latter to individual atoms: Suppplying input would turn NN into tensor
        NN = Dense(i_size_l, activation='tanh', use_bias=True )
        NNelement.append( NN )

    # now append layers
    NNunique.append( NNelement )

# now we have setup all unique NN layers, and we apply them to all atoms in the system
# to create connected tensors 

# note, while NNunique is list of layer objects,
# NNatom_layers is list of layer tensors
NNtotal=[]
inputs=[]
# now apply element specific layer to each atom
for i_atom in range(len(aname)):
    itype = atype[i_atom]
    # input size depends on element, as there could be different number of symmetry functions for each element
    typeNN = NNff.element_force_field[ aname[i_atom] ]
    i_size = len( typeNN.symmetry_functions )
    atom_input = Input(shape=(i_size,))

    NNatom=[]
    # loop over layers
    for i_layer in range(n_layer):

        # here we turn object into tensor by supplying input tensor
        # if first hidden layer, supply 'atom_input' tensor
        if i_layer == 0 :
            layer = NNunique[itype][i_layer]( atom_input )
        else :
            # layer on top of previous layer
            layer = NNunique[itype][i_layer]( layer )

    # append input tensor, and total, layered NN tensor for this atom
    inputs.append( atom_input )
    NNtotal.append(layer)

# now concatenate the atom vectors
NNwhole = concatenate( NNtotal , axis=-1)

#******* output layer *********
# output system energy as sum of atomic energies, so output dimension (units) is 1,
# we are just summing atomic contributions here... K is a keras object set to either tensorflow or theanos
predictions = Lambda(lambda x: K.sum(x, axis=1), output_shape=(1,))(NNwhole)


model = Model(inputs=inputs, outputs=predictions)
model.compile(optimizer='sgd', loss='mean_squared_error')


print( "fitting Neural network to interaction energy data...")
model.fit( sym_input , energy, batch_size=len(energy), epochs=20 )

print( "done fitting Neural network" )
 
print( "summary" )
model.summary()

print( "predictions" )
y = model.predict_on_batch( sym_input )

for i in range(len(energy)):
    print( energy[i] , y[i] )



