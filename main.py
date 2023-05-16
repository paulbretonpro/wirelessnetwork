import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import decode
import binary_transformation as binT
import pdsch


"""
Nous avons séparer le code en plusieurs fichier pour faciliter la maintenance 
durant le TP

decode.py: 
    - bpsk_demode
    - hamming748_decode
    - bin2dec
    - qpsk_demod
    - pdcchu_decode

pdsch.py: 
    - demod
    - fec
    - crc

"""


""" 
2.1 Extraction of the time frequency matrix
"""

# Pour BPSK il faut supprimer les nombres imaginaire, on garde uniquement
# 1 et -1 pour correspondre à la configuration de BPSK
my_data = np.genfromtxt('tfMatrix.csv', delimiter=';')
mat_complex = my_data[:, 0::2] + 1j*my_data[:, 1::2]

# size of matrix [14, 1024]

# Print the matrix of complex symbols with matplotlib
plt.matshow(np.abs(mat_complex), cmap=cm.gray)
# Add title and axis names
plt.title('Matrix of complex symbols')
plt.xlabel('N')
plt.ylabel('Subcarriers')
plt.show()


""" 
2.2 PBCH Decoding
"""

# .1 BPSK decoding

# 1 313, 312 dernière
# one row with 624 bits (only 0 and 1)
m1 = mat_complex[:, range(1, 624//2+1)]
m2 = mat_complex[:, range(1024-(624//2), 1024)]

tfMatrix_short = np.concatenate((m1, m2), axis=1)

# Print the new matrix of complex symbols concatenate : figure 2
plt.matshow(np.abs(tfMatrix_short), cmap=cm.gray)
# Add title and axis names
plt.title('Matrix of new complex symbols')
plt.xlabel('N')
plt.ylabel('Subcarriers')
plt.show()


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

# Print the power repartition : figure 3
powerDistributionGraph( tfMatrix_short )

# On se focalise sur les canaux utiles en supprimant les canaux PPCH et PSCH
qamMatrix = tfMatrix_short[2:, :]

# Print the power repartition without synchronization channel : figure 4
powerDistributionGraph( qamMatrix )

qamSeq = qamMatrix.flatten()
print("Matrice après premiers traitements : ")
print(qamSeq)
print("------------------------------------------------------------------------------")

# Decodage BPSK en utilisant le décodeur défini dans le fichier decode.py
bitSeq = decode.bpsk_demod(qamSeq)
bpsk_first_48_bits = bitSeq[0:48:1]

#Decodage de Hamming du résultat
bitDec = decode.hamming748_decode(bitSeq)
bits48 = decode.hamming748_decode(bpsk_first_48_bits)

#L'identifiant de la cellule correspond au 18 premiers bits et le nombre
#d'utilisateurs aux 6 dernier
cell_ident = decode.bin2dec(bits48[0:18])  # 18 fist bits
nb_users = decode.bin2dec(bits48[18:24])  # last 6 bits

"""
qamSeq = []
for i in range(len(qamMatrix)):
    for el in qamMatrix[i]:
        qamSeq.append(el)
"""

# In a cellular communication network, a cell_ident is a unique identifier assigned
# to a specific cell within the network.
# A cellular network is composed of multiple cells, and each cell has a unique cell identity
# that distinguishes it from other cells in the network.
# cell indent 12345
print("Identité de la cellule :  " + str(cell_ident) )
# 18 users
print("Nombre d'utilisateurs :   " + str(nb_users) )
print("------------------------------------------------------------------------------")

# .3 PBCH decoding


def keepOurUserIndent(userIndent):
    """
    Function to decode and get information of user.
    18 matrix of 48 bits for 18 users
    Args:
        userIndent (int): group number

    Returns:
        object: information of the user
    """
    # the table contain all the data of group
    # we skip the 48 first bits
    start = 48
    for i in range(18):
        #On passe le premier bloc qui contient les informations de la cellule
        end = start + 48
        #On récupère les informations du bloc utilisateur
        user_encoded = bitSeq[start:end:1]
        user = decode.hamming748_decode(user_encoded)
        userId = user[0:8]
        if decode.bin2dec(userId) == userIndent:
            #Dans le cas où le bloc correspond bien à celui recherché
            msc = decode.bin2dec(user[8:10])
            symb_start = decode.bin2dec(user[10:14])
            rb_start = decode.bin2dec(user[14:20])
            harq = decode.bin2dec(user[20:24])
            #On remplit le dictionnaire avec les informations du bloc recherché
            dict_PBCHU = {
                "USER_INDENT": userIndent,
                "MCS": msc,
                "SYMB_START": symb_start,
                "RB_START": rb_start,
                "HARQ": harq
            }

            return dict_PBCHU
        start = end

#On recherche notre bloc
user = keepOurUserIndent(3)

print("Informations concernant l'utilisateur 3 : ")
print(user)
print("------------------------------------------------------------------------------")

"""
2.3 - PDCCH decoding
"""

# .1 MCS decoding

# (voir function qpsk_demod fichier deocde.py)

# .2 PDCCHU decoding

# decode the user's PDCCH channel information from the qamMatrixFlat bit sequence using the values of "SYMB_START"
# and "RB_START" stored in the "user" variable and the value of "MCS" stored in the "user" variable
bitSeq2 = decode.pdcchu_decode(qamSeq[(
    user['SYMB_START']-3) * 624 + (user['RB_START']-1)*12:], user['MCS'])
# decodes the bit sequence "bitSeq2" obtained from the "pdcchu_decode" function using the Hamming code748
pdcchu_decode = decode.hamming748_decode(bitSeq2)

pdcchu = dict()
pdcchu["USER_INDENT"] = decode.bin2dec(pdcchu_decode[0:8])
pdcchu["MCS"] = decode.bin2dec(pdcchu_decode[8:14])
pdcchu["SYMB"] = decode.bin2dec(pdcchu_decode[14:18])
pdcchu["RB"] = decode.bin2dec(pdcchu_decode[18:24])
pdcchu["RB_SIZE"] = decode.bin2dec(pdcchu_decode[24:34])
pdcchu["CRC"] = decode.bin2dec(pdcchu_decode[34:36])

print("Informations contenues dans la bloc PDCCHU de l'utilisateur 3 : ")
print(pdcchu)
print("------------------------------------------------------------------------------")

"""
2.4 PDSCH Decodin
"""
# .1 FEC and MCS overall functions

# (voir fichier pdsch.py)

# .2 PDSCH decoding
symbols = qamSeq[(pdcchu['SYMB']-3)*624+(pdcchu['RB']-1) *
                        12:(pdcchu['SYMB']-3)*624+(pdcchu['RB']-1)*12 + pdcchu['RB_SIZE']*12]
payload = pdsch.fec(pdsch.demod(symbols, pdcchu['MCS']), pdcchu['MCS'])
pdsch_crc = pdsch.crc(payload, pdcchu['CRC'])
if pdsch_crc == 1:
  payload = payload[:len(payload)-(pdcchu['CRC']+1)*8]


 # Assuming the message decoding from QPSK or QAM16 is qamSeq
  # Convert the binary sequence into bytes
  mess = binT.bitToByte(payload)
  # Bytes are "encrypted", uncrypt them
  real_mess = binT.cesarDecode( user['USER_INDENT'], mess)  # USER is your user group
  final_mess = binT.toASCII(real_mess)

  print("Le message reçu est : ")
  print("".join(final_mess))

else:
  print("Erreur de CRC, le message reçu est invalide")