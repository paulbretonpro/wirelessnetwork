import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import decode


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


quamMatrix = tfMatrix_short[2:, :]

qamSeq = []
for i in range(len(quamMatrix)):
    for el in quamMatrix[i]:
        qamSeq.append(el)

bitSeq = decode.bpsk_demod(qamSeq)

bpsk_first_48_bits = bitSeq[0:48:1]

bitDec = decode.hamming748_decode(bitSeq)

bits48 = decode.hamming748_decode(bpsk_first_48_bits)

cell_ident = decode.bin2dec(bits48[0:18])  # 18 fist bits
nb_users = decode.bin2dec(bits48[18:24])  # last 6 bits

print(cell_ident)
print(nb_users)

"""
# PBCHU every 48 bits
PBCHU_1 = bitSeq[48:96]
# print(PBCHU_1.shape)

# List of PBCHU every 48 bits
print("List of PBCHU every 48 bits")
j = 1
for i in range(0, 18, 48):
    PBCHU_Dec = decode.hamming748_decode(bitSeq[i:i+48])
    user_ident = PBCHU_Dec[:8]
    user_ident = decode.bin2dec(user_ident)
    print("(group index,pos) :(%3d," %
          j, ",%3d," % i, ") =%3d," % user_ident)

    j += 1

PBCHU_Dec = decode.hamming748_decode(PBCHU_1)
print(PBCHU_Dec)
print(PBCHU_Dec.shape)
user_ident = PBCHU_Dec[:8]
user_ident = decode.bin2dec(user_ident)
print(user_ident)
MCS_PDCCHU = PBCHU_Dec[8:10]
MCS_PDCCHU = decode.bin2dec(MCS_PDCCHU)
print(MCS_PDCCHU)
SYMB_START_PDCCHU = PBCHU_Dec[10:14]
SYMB_START_PDCCHU = decode.bin2dec(SYMB_START_PDCCHU)
print(SYMB_START_PDCCHU)
RB_START_PDCCHU = PBCHU_Dec[14:20]
RB_START_PDCCHU = decode.bin2dec(RB_START_PDCCHU)
print(RB_START_PDCCHU)
HARQ = PBCHU_Dec[20:24]
HARQ = decode.bin2dec(HARQ)
print(HARQ)
dict_PBCHU = {
    "user_ident": user_ident,
    "MCS_PDCCHU": MCS_PDCCHU,
    "Symb_start_PDCCHU": SYMB_START_PDCCHU,
    "RB_start_PDCCHU": RB_START_PDCCHU,
    "HARQ_PDCCHU": HARQ
}

print(dict_PBCHU)
"""
