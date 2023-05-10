import numpy as np


def bpsk_demod(qamSeq):
    """
    Cette fonction prend en entrée une séquence de symboles QPSK
    modulée avec une démodulation BPSK pour retourner la séquence
    de bits correspondante.

    Args:
    qamSeq (ndarray): Une séquence de symboles QPSK.

    Returns:
    ndarray: Une séquence de bits.
    """
    output = []

    for elem in qamSeq:
        if np.real(elem) > 0:
            bit = 1
        else:
            bit = 0
        output.append(bit)

    return output


def hamming748_decode(bitSeq):
    H = np.array([[0, 0, 0, 1, 1, 1, 1], [
                 0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]])
    res = []
    for i in range(0, len(bitSeq), 8):
        bit_group = bitSeq[i:i+8]
        syndrom = np.dot(H, bit_group[:len(bit_group)-1])
        syndrom = syndrom % 2

        if np.array_equal(syndrom, np.array([0, 0, 0])):
            res += bit_group[:4]
        else:
            sum_parity = np.sum(bit_group[:len(bit_group)-1])
            sum_parity = np.mod(sum_parity, 2)
            if sum_parity == bit_group[7]:
                res += bit_group[:4]
            else:
                binary = syndrom[0]*4 + syndrom[1]*2 + syndrom[2]*1
                bit_group[binary-1] = np.mod(bit_group[binary-1] + 1, 2)
                res += bit_group[:4]
    return res


def bin2dec(nb):
    """
    Transform a binary list to an integer
    """
    n = "0b"
    for b in nb:
        n = n + str(b)
    return int(n, 2)
