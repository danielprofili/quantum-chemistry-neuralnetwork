import matplotlib.pyplot as plt

#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.savefig('plots/test.png')

# plot_atoms(atoms, q_nn, q_qm) plots atoms with names in list 'atoms' and saves
#   the plots to the plots directory as png files.
#   
#   The x-axis for each plot is the QM charge and the y-axis is the NN charge.
#
def plot_atom(atom, q_nn, q_qm, outputdir='plots/'):
    plt.plot(q_qm, q_nn, 'ro')
    plt.xlabel('QM charge')
    plt.ylabel('NN charge')
    plt.title(atom)
    # for debugging
    print('saving plot to ' + outputdir + atom + '.png') 
    plt.savefig(outputdir + atom + '.png')
