import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# extract audio
import sys
from aubio import source, pitch
from glob import glob

print(glob("*"))
filename = r"output.wav"

downsample = 1
samplerate = 44100 // downsample
win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(tolerance)

mic_pitches = []
mic_confidences = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    #pitch = int(round(pitch))
    confidence = pitch_o.get_confidence()
    if confidence < 0.8: pitch = 0.
    # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    mic_pitches += [pitch]
    mic_confidences += [confidence]
    total_frames += read
    if read < hop_s: break

if 0: sys.exit(0)

# Prep for plotting
from numpy import array, ma
import numpy as np
from model_pitch import cleaned_pitches

skip = 1

mic_pitches = array(mic_pitches[skip:])
mic_confidences = array(mic_confidences[skip:])


# plot cleaned up pitches
cleaned_mp = mic_pitches

# arange 
# linspace 


# do not plot pitch == 0 Hz
cleaned_mp = ma.masked_where((cleaned_mp <= 0) | (cleaned_mp <= tolerance), cleaned_mp)

# # pad array so same size
# pad_mic = np.zeros(cleaned_pitches.shape)
# pad_mic[:cleaned_mp.shape[0], :cleaned_mp.shape[1]] = cleaned_mp
# print(pad_mic)