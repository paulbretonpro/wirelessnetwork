import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


my_data = np.genfromtxt('tfMatrix.csv', delimiter=';')
mat_complex = my_data[:, 0::2] + 1j*my_data[:, 1::2]

# size of matrix [14, 1024]

# Print the matrix of complex symbols with matplotlib
plt.matshow(np.abs(mat_complex), cmap=cm.gray)
# Add title and axis names
plt.title('Matrix of complex symbols')
plt.xlabel('N')
plt.ylabel('Subcarriers')
# plt.show()


# 1 313, 312 dernière
m1 = mat_complex[:, range(1, 624//2+1)]
m2 = mat_complex[:, range(1024-(624//2), 1024)]

tfMatrix_short = np.concatenate((m1, m2), axis=1)


# SHAPE 14, 624
# print(np.shape(tfMatrix_short))

# print(tfMatrix_short)


def powerDistributionGraph(Z):
    # Draw the power distribution graph
    fig, ax = plt.subplots()
    cs = ax.contourf(np.linspace(0, len(Z[0]), len(
        Z[0])), np.linspace(0, len(Z), len(Z)), np.abs(Z))
    cbar = fig.colorbar(cs)
    ax.set_title('Répartition de puissance')
    ax.set_xlabel('Fréquence [Hz]')
    ax.set_ylabel('Amplitude [dB]')
    plt.show()


#  powerDistributionGraph(Z)

quamMatrix = tfMatrix_short[3:, :]

# powerDistributionGraph(np.absolute(quamMatrix))

# print(quamMatrix)
