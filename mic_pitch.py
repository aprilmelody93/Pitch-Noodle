# import pyaudio
# import sys
# import numpy as np
# import aubio

# # initialise pyaudio stream
# p = pyaudio.PyAudio()

# # open stream
# buffer_size = 1024
# pyaudio_format = pyaudio.paFloat32
# n_channels = 1
# samplerate = 44100
# stream = p.open(format=pyaudio_format,
#                 channels=n_channels,
#                 rate=samplerate,
#                 input=True,
#                 frames_per_buffer=buffer_size)
# hop_s = 512

# if len(sys.argv) > 1:
#     # record 5 seconds
#     output_filename = sys.argv[1]
#     record_duration = 5 # exit 1
#     outputsink = aubio.sink(sys.argv[1], samplerate)
#     total_frames = 0
# else:
#     # run forever
#     outputsink = None
#     record_duration = None

# # setup pitch
# tolerance = 0.8
# win_s = 4096 # fft size
# hop_s = buffer_size # hop size
# pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
# pitch_o.set_unit("Hz")
# pitch_o.set_tolerance(tolerance)

# pitch_user = []

# print("*** starting recording. Hit Ctrl+C to stop.")
# while True:
#     try:
#         audiobuffer = stream.read(buffer_size)
#         signal = np.fromstring(audiobuffer, dtype=np.float32)

# # Figure out how to add 

#         pitch_user.append(pitch_o(signal)[0])
#         # confidence = pitch_o.get_confidence()

#         # print("{} / {}".format(pitch,confidence))

#         if outputsink:
#             outputsink(signal, len(signal))

#         if record_duration:
#             total_frames += len(signal)
#             if record_duration * samplerate < total_frames:
#                 break
#     except KeyboardInterrupt:
#         print("*** Ctrl+C pressed, exiting")
#         break

# print("*** done recording")
# stream.stop_stream()
# stream.close()
# p.terminate()
# print(pitch_user)


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

skip = 1

mic_pitches = array(mic_pitches[skip:])
mic_confidences = array(mic_confidences[skip:])


# plot cleaned up pitches
cleaned_mic_pitches = mic_pitches

# do not plot pitch == 0 Hz
cleaned_mic_pitches = ma.masked_where((cleaned_mic_pitches <= 0) | (cleaned_mic_pitches <= tolerance), cleaned_mic_pitches)

print(cleaned_mic_pitches)