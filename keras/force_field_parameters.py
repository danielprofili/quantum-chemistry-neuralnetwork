import sys
import numpy as np

""" 
Here we define elemental parameters that are used to construct symmetry functions.
This can be considered a "force field", as the definition and number of symmetry functions
essentially determines the neural network (after fitting/optimization step).

The way this should work is that we should define classes of "force fields", with
each class corresponding to a different collection of symmetry function types and definitions
"""

class elementNN(object):
    """
    this object contains all definitions for element-specific neural network,
    including symmetry function definitions, weight parameters, etc.
    """
    def __init__(self):
        # initialize data structures
        self.symmetry_functions=[]
        self.weights=[]        
        # set default cutoff radius (Rc) for Gaussian symmetry functions
        self.Rc = 11.5 # Bohr

class NNforce_field(object):
    """
    this is neural network force field object, that stores parameters that define
    the atomic neural networks
        aname: list of names of the atoms
    """

    def __init__(self, name, aname=["H", "O"]):
        # setup attributes of force field based on name
        self.aname = aname
        if name is 'FF1':
           self.initialize_FF1()
        elif name is 'FF2':
           self.initialize_FF2()
        elif name is 'FF3':
           self.initialize_FF3()
        else:
           print("force field name ", name , "  is not recognized")
           sys.exit()






    """
                FORCE FIELD DEFINITIONS:
                  note that these methods contain hard-coded parameters
                  which define different force field classes
    """


    def initialize_FF1(self):

        """
        this initializes our first type of neural network
        every type of neural network must have elemental specific parameters
        for symmetry functions
        """

        # create a dictionary to look up force field object for each element
        self.element_force_field={}

        # for now this is just a list of tuples that define the Gaussian width
        # shifts, and cutoff value for each Gaussian symmetry function.  Eventually, this will be
        # a more complicated object...

        # setup force field for oxygen
        oxygenNN = elementNN()
        self.element_force_field["O"] = oxygenNN
        # add list of symmetry function tuples


        oxygenNN.symmetry_functions.append( ( 3.0 , 3.0 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 3.5 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 4.0 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 4.5 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 5.0 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 5.5 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 6.0 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 6.5 ) )
        oxygenNN.symmetry_functions.append( ( 3.0 , 7.0 ) )


       # setup force field for hydrogen
        hydrogenNN = elementNN()
        self.element_force_field["H"] = hydrogenNN
        # add list of symmetry function tuples

        hydrogenNN.symmetry_functions.append( ( 3.0 , 3.0 ) )
        hydrogenNN.symmetry_functions.append( ( 3.0 , 3.5 ) )
        hydrogenNN.symmetry_functions.append( ( 3.0 , 4.0 ) )
        hydrogenNN.symmetry_functions.append( ( 3.0 , 4.5 ) )
        hydrogenNN.symmetry_functions.append( ( 3.0 , 5.0 ) )
        hydrogenNN.symmetry_functions.append( ( 3.0 , 5.5 ) )



    def initialize_FF2(self):

        """
        this initializes our second type of neural network 
        every type of neural network must have elemental specific parameters
        for symmetry functions
        """

        # create a dictionary to look up force field object for each element
        self.element_force_field={}

        # for now this is just a list of tuples that define the Gaussian width
        # shifts, and cutoff value for each Gaussian symmetry function.  Eventually, this will be
        # a more complicated object...

        # setup force field for oxygen
        oxygenNN = elementNN()
        self.element_force_field["O"] = oxygenNN
        # add list of symmetry function tuples


        oxygenNN.symmetry_functions.append( ( 0.5 , 3.0 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 3.0 ) )
        oxygenNN.symmetry_functions.append( ( 2.0 , 3.0 ) )
        oxygenNN.symmetry_functions.append( ( 0.5 , 3.5 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 3.5 ) )
        oxygenNN.symmetry_functions.append( ( 2.0 , 3.5 ) )
        oxygenNN.symmetry_functions.append( ( 0.5 , 4.0 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 4.0 ) )
        oxygenNN.symmetry_functions.append( ( 2.0 , 4.0 ) )
        oxygenNN.symmetry_functions.append( ( 0.5 , 4.5 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 4.5 ) )
        oxygenNN.symmetry_functions.append( ( 2.0 , 4.5 ) )
        oxygenNN.symmetry_functions.append( ( 0.5 , 5.0 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 5.0 ) )
        oxygenNN.symmetry_functions.append( ( 2.0 , 5.0 ) )
        oxygenNN.symmetry_functions.append( ( 0.5 , 5.5 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 5.5 ) )
        oxygenNN.symmetry_functions.append( ( 2.0 , 5.5 ) )
        oxygenNN.symmetry_functions.append( ( 0.5 , 6.0 ) )
        oxygenNN.symmetry_functions.append( ( 1.0 , 6.0 ) )    
        oxygenNN.symmetry_functions.append( ( 2.0 , 6.0 ) )


        # setup force field for hydrogen
        hydrogenNN = elementNN()
        self.element_force_field["H"] = hydrogenNN
        # add list of symmetry function tuples

        hydrogenNN.symmetry_functions.append( ( 0.5 , 2.5 ) )
        hydrogenNN.symmetry_functions.append( ( 1.0 , 2.5 ) )
        hydrogenNN.symmetry_functions.append( ( 2.0 , 2.5 ) )
        hydrogenNN.symmetry_functions.append( ( 0.5 , 3.0 ) )
        hydrogenNN.symmetry_functions.append( ( 1.0 , 3.0 ) )
        hydrogenNN.symmetry_functions.append( ( 2.0 , 3.0 ) )
        hydrogenNN.symmetry_functions.append( ( 0.5 , 3.5 ) )
        hydrogenNN.symmetry_functions.append( ( 1.0 , 3.5 ) )
        hydrogenNN.symmetry_functions.append( ( 2.0 , 3.5 ) )
        hydrogenNN.symmetry_functions.append( ( 0.5 , 4.0 ) )
        hydrogenNN.symmetry_functions.append( ( 1.0 , 4.0 ) )
        hydrogenNN.symmetry_functions.append( ( 2.0 , 4.0 ) )
        hydrogenNN.symmetry_functions.append( ( 0.5 , 4.5 ) )
        hydrogenNN.symmetry_functions.append( ( 1.0 , 4.5 ) )
        hydrogenNN.symmetry_functions.append( ( 2.0 , 4.5 ) )


         



    def initialize_FF3(self):

        """
        this initializes our first type of neural network
        every type of neural network must have elemental specific parameters
        for symmetry functions
        """

        # create a dictionary to look up force field object for each element
        self.element_force_field={}

        # for now this is just a list of tuples that define the Gaussian width
        # shifts, and cutoff value for each Gaussian symmetry function.  Eventually, this will be
        # a more complicated object...


        gauss_width_min = 0.5
        gauss_width_max = 2.0
        num_widths = 10

        cutoff_min = 3.0
        cutoff_max = 8.0
        num_cutoffs = 10

        gauss_vec = np.linspace(gauss_width_min,gauss_width_max,num_widths)
        cutoff_vec = np.linspace(cutoff_min,cutoff_max,num_cutoffs)
        for e in self.aname:
            elemNN = elementNN()
            self.element_force_field[e] = elemNN
            for i in range(num_widths):
                for j in range(num_cutoffs):
                    elemNN.symmetry_functions.append( ( gauss_vec[i], cutoff_vec[j] ) )

        # DEBUG
        #print(elemNN.symmetry_functions)
        #input("debuG")


