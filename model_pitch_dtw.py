import sys
from aubio import source, pitch, onset

# if len(sys.argv) < 2:
#     print("Usage: %s <filename> [samplerate]" % sys.argv[0])
#     sys.exit(1)

from glob import glob
print(glob("*"))
filename = r"april_model.wav"

downsample = 1
samplerate = 44100 // downsample
win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

o = onset("default", win_s, hop_s, samplerate)

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []
onsets = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    confidence = pitch_o.get_confidence()
    if confidence < 0.8: pitch = 0.
    # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

if 0: sys.exit(0)

# Prep for plotting
from numpy import array, ma
import matplotlib.pyplot as plt
import numpy as np

skip = 1
pitches = array(pitches[skip:])
confidences = array(confidences[skip:])
times = [(t * hop_s) / 1000 for t in range(len(pitches))]
pitches = ma.masked_where((pitches <= 0) | (pitches <= tolerance), pitches) # do not plot pitch == 0 Hz

# Load mic_pitches and remove silences
mic_pitches = np.load("mic_pitches.npy")
mic_times = np.load("mic_times.npy")
mic_pitches = ma.masked_where((mic_pitches <= 0) | (mic_pitches <= tolerance), mic_pitches) # do not plot pitch == 0 Hz

# plot pitch
# plt.style.use('seaborn-pastel')
# plt.plot(times, pitches, linewidth=2.0, label="model")
# plt.plot(mic_times, mic_pitches, linewidth=2.0, label="mic")
# plt.xlabel('Time(ms)')
# plt.ylabel('Pitch (Hz)')
# plt.title('Pitch contour comparison')

# plt.legend()
# plt.show()

# run dynamic time warping (DTW)
import numpy as np
import matplotlib.pyplot as plt
import dtwalign

# np.seterr(divide = 'ignore') 
# np.seterr(invalid = 'ignore') 
res = dtwalign.dtw(pitches, mic_pitches)

# dtw distance
print("dtw distance: {}".format(res.distance))
print("dtw normalized distance: {}".format(res.normalized_distance))

# warp mic_pitches to pitches
mic_pitches_warping_path = res.get_warping_path(target="reference")
plt.plot(pitches, linewidth=2.0, label="pitches")
plt.plot(mic_pitches[mic_pitches_warping_path], linewidth=2.0, label="mic_pitches")
plt.legend()
plt.show()