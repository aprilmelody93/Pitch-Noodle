import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import matplotlib.pyplot as plt
import dtwalign


# Read in recorded wav file

# filename1 = "Karen_44100.wav"
# filename2 = "Daniel.wav"


# signal = basic.SignalObj(filename1)
# pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
# pitches = pitches.samp_values
# start = np.argmax(pitches > 0) # find index of first >0 sample
# pitches = pitches[start:] # remove anything before that index
# m_pitches = np.ma.masked_where(pitches <= 0, pitches) # mask 0 pitches (confidence was too low)

# signal = basic.SignalObj(filename2)
# pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
# pitches = pitches.samp_values
# start = np.argmax(pitches > 0)
# pitches = pitches[start:]
# r_pitches = np.ma.masked_where(pitches <= 0, pitches)


# plt.figure(figsize=(25, 3))
# res = dtwalign.dtw(m_pitches, r_pitches, step_pattern="symmetricP2")

# # dtw distance
# print("dtw distance: {}".format(res.distance))
# print("dtw normalized distance: {}".format(res.normalized_distance))

# # warp r_pitches to m_pitches
# r_pitches_warping_path = res.get_warping_path(target="reference")
# plt.xlabel('time (ms)', fontsize=18)
# plt.ylabel('pitch (Hz)', fontsize=18)
# plt.plot(m_pitches, linewidth=2.5, label="Model")
# plt.plot(r_pitches[r_pitches_warping_path], linewidth=2.5, label="Mircophone", color="orange")
# plt.legend()
# plt.show()

# DearPyGUI Imports

import dearpygui.dearpygui as dpg
from dearpygui.core import *
from math import sin

def dtw(sender, data):
    print("Button clicked")

set_primary_window(540, 720)
set_global_font_scale(1.25)


def update_plot_data(sender, app_data, user_data):
    mouse_y = app_data[1]
    plot = user_data[0]
    plot_data = user_data[1]
    if len(plot_data) > 100:
        plot_data.pop(0)
    plot_data.append(sin(mouse_y/30))
    dpg.set_value(plot, plot_data)

    

with dpg.font_registry():
    
    # add font (set as default for entire app)
    dpg.add_font("Arial.ttf", 20, default_font=True)

    # add second font
    secondary_font = dpg.add_font("CAMBRIAZ.TTF", 13)


with dpg.window(label="Intonation Learner", width=540, height=677):
    print("GUI is running..")
    dpg.set_viewport_always_top("Intonation Learner")
    dpg.add_simple_plot(label="Simpleplot1", default_value=(0.3, 0.9, 0.5, 0.3), height=300)
    dpg.add_simple_plot(label="Simpleplot2", default_value=(0.3, 0.9, 2.5, 8.9), overlay="Overlaying", height=180, histogram=True)
    dpg.add_button(label="Stop Recording", callback=dtw)

dpg.start_dearpygui()
