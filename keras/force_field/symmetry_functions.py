import sys
import numpy as np
from numpy import linalg as LA
from numpy import polynomial as poly

"""
these are symmetry functions used as
input to the neural network
"""

def cutoff_function( rmag , Rc ):
    """
    this is cutoff function for
    Gaussian symmetry functions
    """
    if ( rmag <= Rc ):
        fc = 0.5 * ( np.cos( np.pi * rmag / Rc ) + 1 )
    else:
        fc = 0.0

    return fc


def radial_gaussian( rij, i_atom , width, rshift, Rc ):
    """
    this constructs a symmetry function as a sum of gaussians of
    pairwise displacements, namely
    Gi = sum_j_N ( exp( -width*( rij - rshift )**2 )
    """

    #print(" symmetry function ", i_atom )
    #print(rij)
    #input('radial gaussian')

    Gi=0
    for j_atom in range( rij.shape[1] ):

        # DEBUG
        
        fc = cutoff_function( rij[i_atom][j_atom] , Rc )
        Gi = Gi + fc * np.exp(-width * (rij[i_atom][j_atom]-rshift)**2 )
        #print( j_atom , Gi )

    return Gi

def angular_function(rij, i_atom, zeta, lamb, eta):
    return 0

def chebyshev(n, x):
    """ 
    Evaluates the Chebyshev polynomial T_n at x.
    """

    # chebval returns a sum of the form
    # sum_i^n c_i * T_i(x), where c_i's are
    # the elements of a 1 by (n+1) array

    # we only want the value T_n, so set the nth value to 1
    # and keep the rest as zeros
    c = np.zeros(n+1)
    c[n] = 1
    return poly.chebyshev.chebval(x, c)
    






