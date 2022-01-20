import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import mfcc


class MFCCStuff:
    # 22 according to paper (https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.148.5904&rep=rep1&type=pdf)
    order = 22

    def __init__(self, wav_filename):
        (self.rate, self.sig) = wav.read(wav_filename)
        mfcc_features = mfcc(self.sig, self.rate,
                             numcep=MFCCStuff.order)
        self.mfcc = np.array(mfcc_features)  # don't transpose
        self.adjust_matrix()

    def adjust_matrix(self):
        # normalize
        self.mfcc = self.mfcc - self.mfcc.mean(axis=0, keepdims=True)
        self.mfcc = self.mfcc / np.absolute(self.mfcc).max(axis=0)
