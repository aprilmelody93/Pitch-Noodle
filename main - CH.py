import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import matplotlib.pyplot as plt
import dtwalign

'''
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

'''
###############################   GUI   #########################################

from dearpygui.dearpygui import *
import dearpygui.dearpygui as dpg
from dearpygui.core import *
from playsound import playsound
import pyaudio
import aubio

##### Global theme and setup #####

dpg.enable_docking()
dpg.setup_viewport()
dpg.set_viewport_title(title='Welcome')
dpg.set_viewport_width(1600)
dpg.set_viewport_height(900)
dpg.setup_registries()

with dpg.font_registry():
    dpg.add_font("PlayfairDisplay-VariableFont_wght.ttf", 22, default_font=True)
    secondary_font = dpg.add_font("PlayfairDisplay-VariableFont_wght.ttf", 30)

with dpg.theme(default_theme=True) as series_theme:
    dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 107, 53), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (251, 139, 36), category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 3, category=dpg.mvThemeCat_Plots)

##### Required functions ######

def play_model(sender, app_data):
    playsound("Karen.wav")
    # model_file = app_data["file_name_buffer"]
    # playsound(model_file)

def selected_file(sender, app_data, user_data, callback=play_model):
    model_file = app_data["file_name_buffer"]
    print(model_file)



def plot_model(sender, data):
    xaxis = dpg.generate_uuid()
    yaxis = dpg.generate_uuid()

    dpg.fit_axis_data(x_axis)
    dpg.fit_axis_data(y_axis)

    m_pitches_list = m_pitches.tolist(fill_value=0)
    dpg.add_line_series(m_times, m_pitches_list, parent=y_axis)



def record_mic(sender, data):
    p = pyaudio.PyAudio()
    stream = []

    # open stream
    buffer_size = 1024
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    stream = p.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)

    # setup pitch
    tolerance = 0.8
    win_s = 4096 # fft size
    hop_s = buffer_size # hop size
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)


    while True:
        try:
            audiobuffer = stream.read(buffer_size)
            signal = np.fromstring(audiobuffer, dtype=np.float32)

            pitch = pitch_o(signal)[0]
            confidence = pitch_o.get_confidence()

            print("{} / {}".format(pitch,confidence))

        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

# def stop_mic(sender, data):
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

def compare_pitch(sender, data):
    m_pitches_list = m_pitches.tolist(fill_value=0)
    r_pitches_list = r_pitches[r_pitches_warping_path].tolist(fill_value=0)
    len_m = len(m_pitches_list)
    r_times_short = r_times[0:len_m] # Resize because array size has to be the same
    dpg.add_line_series(r_times_short, r_pitches_list, parent=y_axis)


###### GUI for user nav bar ######

with dpg.file_dialog(directory_selector=False, show = False, callback=selected_file) as file_dialog_id:
    dpg.add_file_extension(".*")

with dpg.window(label="User NavBar", width=299, height=900, pos=[0,0]) as user_nav_bar:
    welcome = dpg.add_text("Model Input")
    instructions = dpg.add_text("To start, please upload an audio file.")
    dpg.add_spacing(count=3)
    upload_button = dpg.add_button(label='Upload File', callback= lambda: dpg.show_item(file_dialog_id))
    dpg.add_spacing(count = 5)

    dpg.add_button(label="Play model", callback = play_model)   
    dpg.add_same_line()
    dpg.add_button(label="Model pitch", callback=plot_model)
    dpg.add_spacing(count=10)
    add_separator()
    dpg.add_spacing(count=10)

    record = dpg.add_text("Your Input")
    dpg.add_button(label="Your pitch", callback= compare_pitch)
    dpg.add_spacing(count=5)
    record_instructions = dpg.add_text("Click on the Record button to start,")
    record_instructions2 = dpg.add_text("and Ctrl+c to stop. (buttons not working)")
    dpg.add_button(label="Record", callback = record_mic)
    dpg.add_same_line()
    dpg.add_button(label="Stop")
    dpg.add_spacing(count=10)


    with dpg.theme() as theme_id:
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (62, 146, 204), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (62, 146, 204), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            
    dpg.set_item_theme(user_nav_bar, theme_id)
    dpg.set_item_font(welcome, secondary_font)
    dpg.set_item_font(record, secondary_font)

###### GUI for plot ######

with dpg.window(label="Pitch Plot", width=1250, height=900, pos=[300,0]) as plot_window:

    dpg.add_text("Scroll with your mouse button or click and drag left and right to explore.")
    add_spacing(count=10)

    with dpg.plot(label="Intonation Plot", height=700, width=1200):
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="time (s)")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="pitch (Hz)")

        # dpg.fit_axis_data(x_axis)
        # dpg.fit_axis_data(y_axis)

        # m_pitches_list = m_pitches.tolist(fill_value=0)
        # dpg.add_line_series(m_times, m_pitches_list, parent=y_axis)

        # r_pitches_list = r_pitches[r_pitches_warping_path].tolist(fill_value=0)
        # len_m = len(m_pitches_list)
        # r_times_short = r_times[0:len_m] # Resize because array size has to be the same
        # dpg.add_line_series(r_times_short, r_pitches_list, parent=y_axis)

    with dpg.theme() as theme_plot:
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (28, 93, 153), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (28, 93, 153), category=dpg.mvThemeCat_Core)
            
    dpg.set_item_theme(plot_window, theme_plot)

dpg.start_dearpygui()