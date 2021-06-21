import sys
from aubio import source, pitch

# if len(sys.argv) < 2:
#     print("Usage: %s <filename> [samplerate]" % sys.argv[0])
#     sys.exit(1)

from glob import glob
print(glob("*"))
filename = r"april_mic.wav"

downsample = 1
samplerate = 44100 // downsample
# if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 1.0

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    #pitch = int(round(pitch))
    confidence = pitch_o.get_confidence()
    if confidence < 0.8: pitch = 0.
    # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

if 0: sys.exit(0)

# Prep for plotting
import matplotlib.pyplot as plt
import numpy as np

skip = 1
pitches = np.array(pitches[skip:])
confidences = np.array(confidences[skip:])
times = [(t * hop_s) / 1000 for t in range(len(pitches))]
# pitches = np.ma.masked_where((pitches <= 0) | (pitches <= tolerance), pitches) # do not plot pitch == 0 Hz

# cleaned_pitches = pitches   # plot cleaned up pitches
# cleaned_pitches = np.ma.masked_where((cleaned_pitches <= 0) | (cleaned_pitches <= tolerance), cleaned_pitches) # do not plot pitch == 0 Hz

np.save("User_pitches.npy", pitches)
np.save("User_times.npy", times)

# # plot pitch
# plt.style.use('seaborn-pastel')
# plt.plot(times, cleaned_pitches, linewidth=2.0)
# plt.xlabel('Time(ms)')
# plt.ylabel('Pitch (Hz)')
# plt.title('Pitch contour comparison')

# plt.show()