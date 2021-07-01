import pyaudio  
import wave

import aubio
import numpy as np

def get_pitches(filename, downsample=1, samplerate=44100, win_s=4096, hop_s=512, 
                 min_confidence=0.8, # discard pitches lower than this (what's the range? 0-1? 0-100?)
                 tolerance=0.8,# not clear what tolerance means ...
                method="yin"): #  yinfft, yin, yinfast, fcomb, mcomb, schmitt, specacf
    ''' get list of pitches and confidences for wav file'''

    # downsample
    samplerate = samplerate // downsample
    win_s = win_s // downsample # fft size
    hop_s = hop_s  // downsample # hop size

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    #o = aubio.onset("default", win_s, hop_s, samplerate)

    # https://aubio.org/doc/latest/pitch_8h.html#a42f54a97032b485dab12ab54e0c9fa78
    pitch_o = aubio.pitch(method, win_s, hop_s, samplerate) # 
    pitch_o.set_unit("midi")  #"Hz", "midi", "cent", or "bin"
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)  #tolerance (default is 0.15 for yin and 0.85 for yinfft) 

    pitches = []
    confidences = []
    #onsets = []

    # total number of frames read
    total_frames = 0
    low_confidence_pitches = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]

        # set low confidence pitches to 0 and remove later (seems to be yin or yinfft tolerance threshold)
        confidence = pitch_o.get_confidence()
        if confidence < min_confidence: 
            pitch = 0
            low_confidence_pitches += 1
        # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    # DEBUG
    print("read", total_frames, "frames (", low_confidence_pitches, "with too-low confidence <", min_confidence)

    start_idx = 0
    # find index of first > 0
    for i,p in enumerate(pitches):
        if p > 0:
            start_idx = i
            break

    # do some cleanup and make arrays from lists
    skip = start_idx # why 1?
    pitches = np.array(pitches[skip:])
    confidences = np.array(confidences[skip:])
    pitches = np.ma.masked_where((pitches <= 0) | (pitches <= tolerance), pitches) 
    times = np.array([(t * hop_s) / 1000 for t in range(len(pitches))])

    return (times, pitches, confidences) # we don't need onsets?




'''
# record x seconds
num_secs_str = input("Recording will start after you hit Enter. How many seconds (default 2?")
if num_secs_str == "":  # Just hit return
    num_secs = 2
else:
    num_secs = int(num_secs_str)



mic_record_wav_file(filename, num_secs, CHANNELS=1) # must be mono(?)

print("recorded", num_secs, "into",  filename)
'''


# Read in recorded wav file
#filename = "output.wav"
filename1 = "Karen.wav"
#filename = "lala1.wav"
r_times, r_pitches, r_confidences = get_pitches(filename1, min_confidence=0.8, tolerance=0.8, method="yin")
#r_times, r_pitches, r_confidences = get_pitches(filename, min_confidence=0.7, tolerance=0.8, method="yin", win_s=1764, hop_s=441)
#r_times, r_pitches, r_confidences = get_pitches(filename, min_confidence=0.8, tolerance=0.8, method="yinfft")
#r_times, r_pitches, r_confidences = get_pitches(filename, min_confidence=0.8, tolerance=0.8, method="mcomb")
print(filename1, len(r_pitches), len(r_times))

# read in model file
filename2 = "Sam.wav"
#filename = "april_model.wav"
#filename = "lala1.wav"
m_times, m_pitches, m_confidences = get_pitches(filename2, min_confidence=0.8, tolerance=0.8, method="yin")
print(filename2, len(m_pitches), len(m_times))


# using yappt instead
'''
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic

signal = basic.SignalObj('Karen.wav')
pitches = pYAAPT.yaapt(signal, f0_min=100.0, f0_max=240.0, frame_length=40, tda_frame_length=40, frame_space=5.0)
pitches = pitches.samp_values
r_pitches = np.ma.masked_where(pitches <= 0, pitches)

signal = basic.SignalObj('Sam_.wav')
pitches = pYAAPT.yaapt(signal, f0_min=100.0, f0_max=240.0, frame_length=40, tda_frame_length=40, frame_space=5.0)
pitches = pitches.samp_values
m_pitches = np.ma.masked_where(pitches <= 0, pitches)
'''

import matplotlib.pyplot as plt

# plot both pitches
plt.style.use('seaborn-pastel')
plt.figure(figsize=(20, 3))
#plt.plot(m_times, m_pitches, linewidth=2.5, label="model")
#plt.plot(r_times, r_pitches, linewidth=2.5, label="rec")
plt.plot(m_pitches, linewidth=2.5, label=filename2)
plt.plot(r_pitches, linewidth=2.5, label=filename1)

#plt.xlabel('Time (s)')
plt.ylabel('Pitch (Midi)')
plt.title('Pitch contour comparison')

plt.legend()
plt.show()
