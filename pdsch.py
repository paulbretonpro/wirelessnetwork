from crc import *
import decode
import qam16_demod
import numpy as np
import sk_dsp_comm.fec_conv as fecc


def demod(qamSeq, mcs):
    if mcs == 5 or mcs == 25:
        return decode.bpsk_demod(qamSeq)
    elif mcs == 6 or mcs == 26:
        return decode.qpsk_demod(qamSeq)
    elif mcs == 7 or mcs == 27:
        return qam16_demod.qam16_demod(qamSeq)


def fec(qamSeq, mcs):
    if mcs >= 25 and mcs <= 27:
        return decode.hamming748_decode(qamSeq)
    else:
        cc1 = fecc.FECConv(('1011011', '1111001'), 6)
        return cc1.viterbi_decoder(np.array(qamSeq).astype(int), 'hard')


def crc(qamSeq, crc):
    crcSize = (crc + 1) * 8
    poly = get_crc_poly(crcSize)
    return crc_decode(qamSeq, poly)  # 1 good or 0 bad
