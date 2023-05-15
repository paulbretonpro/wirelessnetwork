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
    """
    An error corrector capable of detecting and correcting single bit errors. 
    The three coded bits are chosen so that each bit position in the code word is covered 
    by a unique combination of bits, as well as a parity bit.
    """
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


def qpsk_demod(qamSeq):
    """
    Implement a QPSK demodulator
    it takes a complex-valued input qamSeq and produces a binary sequence as output. 
    """
    res = []
    for i in range(qamSeq.shape[0]):
        if qamSeq[i].real > 0:
            if qamSeq[i].imag > 0:
                res += [1, 1]
            else:
                res += [1, 0]
        else:
            if qamSeq[i].imag > 0:
                res += [0, 1]
            else:
                res += [0, 0]
    return res


def pdcchu_decode(stream, MCS):
    if MCS == 0:
        return bpsk_demod(stream[:72])
    elif MCS == 2:
        return qpsk_demod(stream[:72])
