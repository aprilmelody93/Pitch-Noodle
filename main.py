import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import matplotlib.pyplot as plt
import dtwalign


# Read in recorded wav file

filename1 = "Karen_44100.wav"
filename2 = "Daniel.wav"
hop_s = 512

signal = basic.SignalObj(filename1)
pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
pitches = pitches.samp_values
start = np.argmax(pitches > 0) # find index of first >0 sample
pitches = pitches[start:] # remove anything before that index
m_pitches = np.ma.masked_where(pitches <= 0, pitches) # mask 0 pitches (confidence was too low)
m_times = [(t * hop_s) / 1000 for t in range(len(pitches))]

signal = basic.SignalObj(filename2)
pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
pitches = pitches.samp_values
start = np.argmax(pitches > 0)
pitches = pitches[start:]
r_times = [(t * hop_s) / 1000 for t in range(len(pitches))]
r_pitches = np.ma.masked_where(pitches <= 0, pitches)


plt.figure(figsize=(25, 3))
res = dtwalign.dtw(m_pitches, r_pitches, step_pattern="symmetricP2")

# dtw distance
print("dtw distance: {}".format(res.distance))
print("dtw normalized distance: {}".format(res.normalized_distance))

# # warp r_pitches to m_pitches
r_pitches_warping_path = res.get_warping_path(target="reference")
# plt.xlabel('time (ms)', fontsize=18)
# plt.ylabel('pitch (Hz)', fontsize=18)
# plt.plot(m_pitches, linewidth=2.5, label="Model")
# plt.plot(r_pitches[r_pitches_warping_path], linewidth=2.5, label="Mircophone", color="orange")
# plt.legend()
# plt.show()

###############################   GUI   #########################################

from dearpygui.dearpygui import *
import dearpygui.dearpygui as dpg
from dearpygui.core import *
from math import sin

dpg.enable_docking()
dpg.setup_viewport()
dpg.set_viewport_title(title='Welcome')
dpg.set_viewport_width(1500)
dpg.set_viewport_height(900)

xaxis = dpg.generate_uuid()
yaxis = dpg.generate_uuid()

def Record(sender, data):
    print("Record Button clicked")

with dpg.font_registry():
    dpg.add_font("AGaramondPro-Bold.otf", 20, default_font=True)
    secondary_font = dpg.add_font("Arial.ttf", 13)


    # def plot_callback(sender, data):
#     add_plot_axis(mvXAxis, label="x")
#     add_plot_axis(mvYAxis, label="y")
#     add_line_series(m_times, m_pitches, weight=2, color=[0, 0, 255, 100], parent=last_item())
#     add_shade_series(r_times, r_pitches[r_pitches_warping_path], weight=2, fill=[255, 0, 0, 100])

with dpg.window():
    with dpg.plot(label="Intonation Plot", height=700, width=1400):
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="x")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="y")

        dpg.fit_axis_data(x_axis)
        dpg.fit_axis_data(y_axis)

        m_pitches_list = m_pitches.tolist(fill_value=0)
        dpg.add_line_series(m_times, m_pitches, parent=y_axis)

        r_pitches_list = r_pitches[r_pitches_warping_path].tolist(fill_value=0)
        dpg.add_line_series(r_times, r_pitches_list, parent=y_axis)
        # add_button(label="Plot data", callback=plot_callback)


dpg.start_dearpygui()
