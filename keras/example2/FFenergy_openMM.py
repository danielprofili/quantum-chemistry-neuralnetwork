from __future__ import print_function
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
import routines2 as routines

#**********************************************
# this routine uses OpenMM to evaluate energies of SAPT-FF force field
# we use the DrudeSCFIntegrator to solve for equilibrium Drude positions.
# positions of atoms are frozen by setting mass = 0 in .xml file
#**********************************************

def compute_SAPT_FF_energies( xyz , pdbtemplate, residuexml, saptxml ):

    # xyz coordinates input in bohr, convert to nm
    print("converting xyz coordinates from Bohr to nm in compute_SAPT_FF_energies ...")
    xyz = xyz / 1.88973 / 10.0

    # this is used for topology, coordinates are not used...
    pdb = PDBFile( pdbtemplate )

    # Use the SCF integrator to optimize Drude positions 
    integ_md = DrudeSCFIntegrator(0.001*picoseconds)

    pdb.topology.loadBondDefinitions( residuexml )
    pdb.topology.createStandardBonds();
    modeller = Modeller(pdb.topology, pdb.positions)
    forcefield = ForceField( saptxml )
    modeller.addExtraParticles(forcefield)

    # by default, no cutoff is used, so all interactions are computed
    system = forcefield.createSystem(modeller.topology, constraints=None, rigidWater=True)
    nbondedForce = [f for f in [system.getForce(i) for i in range(system.getNumForces())] if type(f) == NonbondedForce][0]
    customNonbondedForce = [f for f in [system.getForce(i) for i in range(system.getNumForces())] if type(f) == CustomNonbondedForce][0]

    for i in range(system.getNumForces()):
        f = system.getForce(i)
        type(f)
        f.setForceGroup(i)


    platform = Platform.getPlatformByName('CPU')
    simmd = Simulation(modeller.topology, system, integ_md, platform)


    #************************* now compute energies from force field *****************************


    # now loop over data points and compute interaction energies
    print( ' Computing SAPT-FF force field energy...' )

    eSAPTFFdata=[]
    for i in range(len(xyz)):
        # set coordinates in modeller object,
        # need to use modeller object as this is where initial shell postions are generated
        modeller_pos = routines.set_modeller_coordinates( pdb , modeller ,  xyz[i] )

        # add dummy site and shell initial positions
        modeller_pos.addExtraParticles(forcefield)   

        # compute energies
        simmd.context.setPositions(modeller_pos.positions)

        # integrate one step to optimize Drude positions
        simmd.step(1)

        state = simmd.context.getState(getEnergy=True,getForces=True,getPositions=True)

        # if we want to print this comparision, need to input energy list to this subroutine
        eSAPTFF = state.getPotentialEnergy()
        # SAPT energy from input file, convert mH to kJ/mol
        #eSAPT = energy[i] * 2.6255
        #print( eSAPT , eSAPTFF )

        eSAPTFFdata.append( float(eSAPTFF._value) )


    return eSAPTFFdata
