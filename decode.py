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
