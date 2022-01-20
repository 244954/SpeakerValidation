import sounddevice as sd
import scipy.io.wavfile as wav


def record(filename: str, directory=''):
    fs = 44100  # Sample rate
    seconds = 2  # Duration of recording
    if len(directory) > 0 and directory[-1] != '/':
        directory += '/'

    print("Start")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    wav.write('{}voice_{}.wav'.format(directory, filename), fs, myrecording)  # Save as WAV file


if __name__ == '__main__':
    record('Mateusz10')
