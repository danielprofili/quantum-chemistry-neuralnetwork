import sys
import numpy as np

""" 
Here we define elemental parameters that are used to construct symmetry functions.
This can be considered a "force field", as the definition and number of symmetry functions
essentially determines the neural network (after fitting/optimization step).

The way this should work is that we should define classes of "force fields", with
each class corresponding to a different collection of symmetry function types and definitions
"""

class ElementNN(object):
    """
    this object contains all definitions for element-specific neural network,
    including symmetry function definitions, weight parameters, etc.
    """
    def __init__(self, atom_type):
        # initialize data structures
        self.symmetry_functions=[]
        self.weights=[]        
        # set default cutoff radius (Rc) for Gaussian symmetry functions
        self.Rc = 3 # angstroms 
        # type of atom (i.e. "N", "S", "O", "C", or "F"
        if atom_type not in ['N', 'S', 'O', 'C', 'F']:
            raise ValueError('Atom type can only be N, S, O, C, or F')
        self.atom_type = atom_type

class NNforce_field(object):
    """
    this is neural network force field object, that stores parameters that define
    the atomic neural networks
    """

    def __init__(self, name, atypename):
        # setup attributes of force field based on name
        if name is 'FF1':
           self.initialize_FF1(atypename)
        else:
           print("force field name ", name , "  is not recognized")
           sys.exit()






    """
                FORCE FIELD DEFINITIONS:
                  note that these methods contain hard-coded parameters
                  which define different force field classes
    """


    def initialize_FF1(self, atoms_list):

        """
        this initializes our first type of neural network 
        every type of neural network must have elemental specific parameters
        for symmetry functions
        """

        # create a dictionary to look up force field object for each element
        self.element_force_field={}
        
        for atom in atoms_list:
            elem = ElementNN(atom)
            self.element_force_field[atom] = elem

            # range for shift is [2, 5] angstroms
            # range for width is [1, 4] ang^-1
            for s in np.arange(2, 5.5, 0.5):
                for w in np.arange(1, 5.5, 0.5):
                    elem.symmetry_functions.append((s, w))
        # for now this is just a list of tuples that define the Gaussian width
        # shifts, and cutoff value for each Gaussian symmetry function.  Eventually, this will be
        # a more complicated object...

