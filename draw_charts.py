from record import record
import scipy.io.wavfile as wav
from MFCCStuff import mfcc
import matplotlib.pyplot as plt
import numpy as np


# https://moonbooks.org/Articles/How-to-change-imshow-aspect-ratio-and-fit-the-colorbar-size-in-matplotlib-/
def forceAspect(axx, aspect):
    im = axx.get_images()
    extent = im[0].get_extent()
    axx.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)


if __name__ == '__main__':
    name = "demo"
    record(name, directory='wavs/')

    (rate, sig) = wav.read("wavs/voice_{}.wav".format(name))
    mfcc_feat = mfcc(sig, rate,
                     numcep=22)  # 22 according to paper (https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.148.5904&rep=rep1&type=pdf)
    print(mfcc_feat.shape)
    mfcc = mfcc_feat.T

    fig = plt.figure()
    ax = fig.add_subplot(111)
    img = plt.imshow(mfcc, extent=[0, 3, 22, 0])
    forceAspect(ax, aspect=1.0)

    v1 = np.linspace(mfcc.min(), mfcc.max(), 10, endpoint=True)
    cb = plt.colorbar(ticks=v1)
    cb.ax.set_yticklabels(["{:4.2f}".format(i) for i in v1], fontsize='7')

    plt.savefig("charts/MFCC_{}".format(name))
    plt.show()

    print(mfcc_feat)
    print(mfcc_feat.shape)
