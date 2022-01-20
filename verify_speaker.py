from SVMStuff import *
from record import record
from trim_wavs import trim


def generate_SVM():
    target_mfcc = np.empty((0, 22))

    impostor_mfcc = np.empty((0, 22))

    test_mfcc_target = []
    test_mfcc_impostor = []

    for i in range(1, 11):
        (rate, sig) = wav.read("trimmed_sounds/voice_Mateusz{}.wav".format(i))
        MFCC = MFCCStuff("trimmed_sounds/voice_Mateusz{}.wav".format(i))
        if i == 2:
            m1 = MFCCStuff("trimmed_sounds/voice_Mateusz{}.wav".format(4))
            test_mfcc_target = m1.mfcc
        target_mfcc = np.concatenate((target_mfcc, MFCC.mfcc), axis=0)

    for i in [1, 2, 3]:
        (rate, sig) = wav.read("trimmed_sounds/voice_Justyna{}.wav".format(i))
        MFCC = MFCCStuff("trimmed_sounds/voice_Justyna{}.wav".format(i))
        if i == 2:
            m1 = MFCCStuff("trimmed_sounds/voice_Kamil{}.wav".format(2))
            test_mfcc_impostor = m1.mfcc
        impostor_mfcc = np.concatenate((impostor_mfcc, MFCC.mfcc), axis=0)

    for i in [1, 2, 3]:
        (rate, sig) = wav.read("trimmed_sounds/voice_Kamil{}.wav".format(i))
        MFCC = MFCCStuff("trimmed_sounds/voice_Kamil{}.wav".format(i))
        impostor_mfcc = np.concatenate((impostor_mfcc, MFCC.mfcc), axis=0)

    for i in [1, 2, 3, 4, 5]:
        (rate, sig) = wav.read("trimmed_sounds/voice_FakeSound{}.wav".format(i))
        MFCC = MFCCStuff("trimmed_sounds/voice_FakeSound{}.wav".format(i))
        impostor_mfcc = np.concatenate((impostor_mfcc, MFCC.mfcc), axis=0)

    for i in [1, 2, 3, 4, 5]:
        (rate, sig) = wav.read("trimmed_sounds/voice_Grzegorz{}.wav".format(i))
        MFCC = MFCCStuff("trimmed_sounds/voice_Grzegorz{}.wav".format(i))
        impostor_mfcc = np.concatenate((impostor_mfcc, MFCC.mfcc), axis=0)

    for i in ['Marcin', 'Sylwia', 'Ania']:
        (rate, sig) = wav.read("trimmed_sounds/voice_{}.wav".format(i))
        MFCC = MFCCStuff("trimmed_sounds/voice_{}.wav".format(i))
        impostor_mfcc = np.concatenate((impostor_mfcc, MFCC.mfcc), axis=0)

    SVM = SVMStuff(target_mfcc, impostor_mfcc)
    return SVM


def test(SVM, verbose=False):

    mfcc_test = MFCCStuff("voice_Test{}.wav".format(1))
    pred = SVM.predict(mfcc_test.mfcc)
    unique, counts = np.unique(pred, return_counts=True)
    d = dict(zip(unique, counts))
    if verbose:
        if 1 in d and -1 in d and d[1] > d[-1]:
            print('Rozpoznano użytkownika')
        elif 1 in d and -1 not in d:
            print('Rozpoznano użytkownika')
        else:
            print('Nie rozpoznano użytkownika')
        print(d)
    return d


if __name__ == '__main__':
    SVM = generate_SVM()
    record("Test1", directory='')
    trim("Test1")
    test(SVM, verbose=True)

