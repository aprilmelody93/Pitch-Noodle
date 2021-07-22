import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import matplotlib.pyplot as plt
import dtwalign
import keyboard
import mouse


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
import numpy.ma as ma
from playsound import playsound
import pyaudio
import aubio
import wave


# import debugpy
# debugpy.connect(('localhost',5678))


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
    dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 5, category=dpg.mvThemeCat_Plots)

with dpg.value_registry():
    m_pitches = dpg.add_float_vect_value(default_value=[])
    #dpg.set_value(m_pitches, [1.2, 3.4])


##### Global Variables ######
model_pitches = None # Global var of model pitches as list
pitches = None
model_file_name = None
mic_file_name = None

##### Model Pitch Callbacks ######

def plot_model(sender, app_data, user_data):

    global model_pitches, model_file_name

    xaxis = dpg.generate_uuid()
    yaxis = dpg.generate_uuid()

    dpg.fit_axis_data(x_axis)
    dpg.fit_axis_data(y_axis)

    times = list(range(0, len(model_pitches), 1))
    dpg.add_line_series(times, model_pitches, label=model_file_name, parent=y_axis)
    dpg.add_button(label="Delete" + model_file_name, user_data = dpg.last_item(), parent=dpg.last_item(), callback=lambda s, a, u: dpg.delete_item(u))

def play_file(sender, app_data):

    global model_file_name

    if model_file_name != None:
        playsound(model_file_name)


def upload_file_cb(sender, app_data, user_data):

    global model_pitches, model_file_name

    # debugpy.breakpoint() # Must use this method to get breakpoint inside a callback
    model_file_name = app_data["file_name_buffer"]
    print(model_file_name)
    signal = basic.SignalObj(model_file_name)
    pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
    pitches = pitches.samp_values
    start = np.argmax(pitches > 0) # find index of first >0 sample
    pitches = pitches[start:] # remove anything before that index
    model_pitches = ma.masked_where (pitches <=0, pitches)
    model_pitches[model_pitches <= 0] = np.nan #masking 0 values with NaN so that it doesn't plot

##### Mic Pitch Callbacks ######

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
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    while True:
        try:
            audiobuffer = stream.read(buffer_size)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)
            pitch = pitch_o(signal)[0]
            # mic_pitches.append(pitch_o(signal)[0])
            confidence = pitch_o.get_confidence()
            print("{} / {}".format(pitch,confidence))
            if mouse.is_pressed(button='left'):
                print("Recording stopped!")
                break

        except:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(type(stream), stream)


    # wf = wave.open(mic_file_name, 'wb')
    # wf.setnchannels(n_channels)
    # wf.setsampwidth(p.get_sample_size(format))
    # wf.setframerate(samplerate)
    # wf.writeframes(b''.join(mic_pitches))
    # wf.close()

def stop_mic(sender, data):
    global mic_file_name

    mic_file_name = "user_output.wav"

def your_pitch(sender, data):

    global mic_pitches, mic_file_name

    signal = basic.SignalObj(mic_file_name)
    pitches = pYAAPT.yaapt(signal, f0_min=50.0, f0_max=500.0, frame_length=40, tda_frame_length=40, frame_space=5)
    pitches = pitches.samp_values
    start = np.argmax(pitches > 0)
    pitches = pitches[start:]
    hop_s = 512
    r_times = [(t * hop_s) / 1000 for t in range(len(pitches))]
    mic_pitches = np.ma.masked_where(pitches <= 0, pitches)

    # dtw distance
    res = dtwalign.dtw(m_pitches, mic_pitches, step_pattern="symmetricP2")
    print("dtw distance: {}".format(res.distance))
    print("dtw normalized distance: {}".format(res.normalized_distance))

    # dtw warp r_pitches to m_pitches
    mic_pitches_warping_path = res.get_warping_path(target="reference")

    # Resize array and print pitch
    m_pitches_list = mic_pitches.tolist(fill_value=0)
    mic_pitches_list = mic_pitches[mic_pitches_warping_path].tolist(fill_value=0)
    len_m = len(m_pitches_list)
    r_times_short = r_times[0:len_m] # Resize because array size has to be the same
    dpg.add_line_series(r_times_short, mic_pitches_list, parent=y_axis)

def play_your_file(sender, data):
    global mic_file_name
    print(mic_file_name)

    if mic_file_name != None:
        playsound(mic_file_name)


###### Nav Bar Settings ######

with dpg.file_dialog(directory_selector=False, show = False, callback=upload_file_cb) as file_dialog_id:
    dpg.add_file_extension(".wav")
    

with dpg.window(label="User NavBar", width=299, height=900, pos=[0,0]) as user_nav_bar:
    welcome = dpg.add_text("Model Input")
    instructions = dpg.add_text("To start, please upload an audio file.")
    dpg.add_spacing(count=3)
    upload_button = dpg.add_button(label='Upload file', callback= lambda: dpg.show_item(file_dialog_id))
    dpg.add_same_line()

    play_model_button_id = dpg.add_button(label="Play file", callback=play_file)   
    dpg.add_spacing(count=10)
    dpg.add_separator()  # CH fix
    dpg.add_spacing(count=10)

    record = dpg.add_text("Your Input")
    record_instructions = dpg.add_text("Click on the Record button to start,")
    record_instructions2 = dpg.add_text("and the Stop button to stop.")
    dpg.add_spacing(count=3)
    dpg.add_button(label="Record", callback = record_mic)
    dpg.add_same_line()
    dpg.add_button(label="Stop", callback = stop_mic)
    dpg.add_same_line()
    dpg.add_button(label="Play", callback = play_your_file)
    dpg.add_spacing(count=10)


    with dpg.theme() as theme_id:
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (62, 146, 204), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (62, 146, 204), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            
    dpg.set_item_theme(user_nav_bar, theme_id)
    dpg.set_item_font(welcome, secondary_font)
    dpg.set_item_font(record, secondary_font)

###### Plot Settings ######

with dpg.window(label="Pitch Plot", width=1250, height=900, pos=[300,0]) as plot_window:

    tips = dpg.add_text("Here are some basic tips:")
    dpg.add_text("1. Scroll with your mouse button or click and drag left and right to explore.")
    dpg.add_text("2.Left click on the legend to show/hide.")
    dpg.add_text("3. Right click on the legend to delete.")
    dpg.add_spacing(count=5)

    with dpg.plot(label="Intonation Plot", height=600, width=1200):
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="time (s)", no_tick_labels = True)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="pitch (Hz)", no_tick_labels = False)

    with dpg.theme() as theme_plot:
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (28, 93, 153), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (28, 93, 153), category=dpg.mvThemeCat_Core)
    
    dpg.add_button(label="Model pitch", user_data=m_pitches, callback=plot_model)
    dpg.add_same_line()
    dpg.add_button(label="Your pitch", callback= your_pitch)
            
    dpg.set_item_theme(plot_window, theme_plot)
    dpg.set_item_font(tips, secondary_font)

dpg.start_dearpygui()
