import sys
from aubio import source, pitch

# if len(sys.argv) < 2:
#     print("Usage: %s <filename> [samplerate]" % sys.argv[0])
#     sys.exit(1)

from glob import glob
print(glob("*"))
filename = r"HowAreYou_Mono.wav"

downsample = 1
samplerate = 44100 // downsample
# if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

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
from numpy import array, ma
import matplotlib.pyplot as plt

skip = 1
pitches = array(pitches[skip:])
confidences = array(confidences[skip:])
times = [(t * hop_s) / 1000 for t in range(len(pitches))]
cleaned_pitches = pitches   # plot cleaned up pitches
cleaned_pitches = ma.masked_where((cleaned_pitches <= 0) | (cleaned_pitches <= tolerance), cleaned_pitches) # do not plot pitch == 0 Hz

# plot pitch
plt.style.use('seaborn-pastel')
plt.plot(times, cleaned_pitches, linewidth=2.0)
plt.xlabel('Time(ms)')
plt.ylabel('Pitch (Hz)')
plt.title('Pitch contour comparison')

plt.show()