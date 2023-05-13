import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import decode
import binary_transformation as binT
import pdsch

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


qamMatrix = tfMatrix_short[2:, :]

qamSeq = []
for i in range(len(qamMatrix)):
    for el in qamMatrix[i]:
        qamSeq.append(el)

bitSeq = decode.bpsk_demod(qamSeq)

bpsk_first_48_bits = bitSeq[0:48:1]

bitDec = decode.hamming748_decode(bitSeq)

bits48 = decode.hamming748_decode(bpsk_first_48_bits)

cell_ident = decode.bin2dec(bits48[0:18])  # 18 fist bits
nb_users = decode.bin2dec(bits48[18:24])  # last 6 bits

print(cell_ident)
print(nb_users)


def keepOurUserIndent(userIndent):
    start = 48
    for i in range(18):
        end = start + 48
        user_encoded = bitSeq[start:end:1]
        user = decode.hamming748_decode(user_encoded)
        userId = user[0:8]
        if decode.bin2dec(userId) == userIndent:
            msc = decode.bin2dec(user[8:10])
            symb_start = decode.bin2dec(user[10:14])
            rb_start = decode.bin2dec(user[14:20])
            harq = decode.bin2dec(user[20:24])
            dict_PBCHU = {
                "USER_INDENT": userIndent,
                "MCS": msc,
                "SYMB_START": symb_start,
                "RB_START": rb_start,
                "HARQ": harq
            }

            return dict_PBCHU
        start = end


user = keepOurUserIndent(3)


# 2.3 - PDCCH decoding

qamMatrixFlat = qamMatrix.flatten()
bitSeq2 = decode.pdcchu_decode(qamMatrixFlat[(
    user['SYMB_START']-3) * 624 + (user['RB_START']-1)*12:], user['MCS'])

# 2.3.2 PDCCHU decoding
pdcchu_decode = decode.hamming748_decode(bitSeq2)

pdcchu = dict()
pdcchu["USER_INDENT"] = decode.bin2dec(pdcchu_decode[0:8])
pdcchu["MCS"] = decode.bin2dec(pdcchu_decode[8:14])
pdcchu["SYMB"] = decode.bin2dec(pdcchu_decode[14:18])
pdcchu["RB"] = decode.bin2dec(pdcchu_decode[18:24])
pdcchu["RB_SIZE"] = decode.bin2dec(pdcchu_decode[24:34])
pdcchu["CRC"] = decode.bin2dec(pdcchu_decode[34:36])

print(pdcchu)

# 2.4.1 FEC and MCS overall functions

# (voir fichier pdsch.py)

# 2.4.2 PDSCH decoding
symbols = qamMatrixFlat[(pdcchu['SYMB']-3)*624+(pdcchu['RB']-1) *
                        12:(pdcchu['SYMB']-3)*624+(pdcchu['RB']-1)*12 + pdcchu['RB_SIZE']*12]
payload = pdsch.fec(pdsch.demod(symbols, pdcchu['MCS']), pdcchu['MCS'])
pdsch_crc = pdsch.crc(payload, pdcchu['CRC'])
if pdsch_crc == 1:
    payload = payload[:len(payload)-(pdcchu['CRC']+1)*8]


# Assuming the message decoding from QPSK or QAM16 is qamSeq
# Convert the binary sequence into bytes
mess = binT.bitToByte(payload)
# Bytes are "encrypted", uncrypt them
real_mess = binT.cesarDecode(
    user['USER_INDENT'], mess)  # USER is your user group
final_mess = binT.toASCII(real_mess)

print("".join(final_mess))
