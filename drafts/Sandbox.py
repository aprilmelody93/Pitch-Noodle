import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
from dearpygui.dearpygui import *
from dearpygui.core import *
import numpy.ma as ma
from matplotlib import pyplot as plt


signal = basic.SignalObj('model_files/E_Yao2.wav')
pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
pitches.set_values(pitches.samp_values, len(pitches.values), interp_tech='spline')
model_pitches = pitches.values
print(type(model_pitches))
model_pitches = ma.masked_where(model_pitches <=0, model_pitches)
print(type(model_pitches))
# model_pitches[model_pitches <= 0] = np.nan #masking 0 values with NaN so that it doesn't plot
times = list(range(0, len(model_pitches), 1))
plt.plot(times, model_pitches, color='red')


plt.xlabel('samples', fontsize =18)
plt.ylabel('pitch (Hz)', fontsize=18)
plt.legend(loc='upper right')
axes = plt.gca()
# axes.set_ylim(50, 500)

plt.show()