from pydub import AudioSegment
import os


def detect_leading_silence(sound, silence_threshold=-85.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


if __name__ == '__main__':
    rootdir = 'wavs'
    extensions = ('.wav', '.mp3')

    AudioSegment.converter = "C:/Program Files/ffmpeg/bin/ffmpeg"
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext in extensions:
                path = os.path.join(subdir, file)

                sound = AudioSegment.from_wav(file=path)

                start_trim = detect_leading_silence(sound)
                end_trim = detect_leading_silence(sound.reverse())

                duration = len(sound)
                trimmed_sound = sound[start_trim:duration - end_trim]
                export_path = os.path.join('trimmed_sounds', file)
                trimmed_sound.export(export_path, format="wav")
