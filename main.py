import numpy as np
import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
import mouse
from dearpygui.dearpygui import *
import dearpygui.dearpygui as dpg
from dearpygui.core import *
import numpy.ma as ma
import pyaudio
from playsound import playsound
import wave
import tempfile
import os

###############################   GUI   #########################################

##### Global theme and setup #####

setup_viewport()
set_viewport_title(title='Welcome')
set_viewport_width(1600)
set_viewport_height(900)
setup_registries()


with dpg.font_registry():
    dpg.add_font("fonts\Playfair.ttf", 22, default_font=True)
    secondary_font = dpg.add_font("fonts\Playfair.ttf", 30)

with dpg.theme(default_theme=True) as series_theme:
    dpg.add_theme_color(dpg.mvThemeCol_Button, (245, 184, 65), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (213, 146, 11), category=dpg.mvThemeCat_Core)
    dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 5, category=dpg.mvThemeCat_Plots)
    # dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, 20, category=dpg.mvThemeCat_Plots)

with dpg.theme() as not_enabled:
    dpg.add_theme_color(dpg.mvThemeCol_Button, (213, 146, 11), category=dpg.mvThemeCat_Core)
    dpg.add_theme_color(dpg.mvThemeCol_Text, (97, 66, 5), category=dpg.mvThemeCat_Core)

with dpg.value_registry():
    m_pitches = dpg.add_float_vect_value(default_value=[])

##### Global Variables and temporary directory######
model_pitches = None # Global var of model pitches as list
pitches = None
model_file_name = None
file_path = None
mic_file_name = None
recording_counter = 0
group_id = 0
times = None

tmpdir = tempfile.TemporaryDirectory(prefix = "tmp_", dir = ".")

##### Model Pitch Callbacks ######

def plot_model(sender, app_data, user_data):
    """Takes in times and model_pitches; return a line series."""

    model_file_name = user_data[0].replace(".wav", "")
    model_pitches = user_data[2]
    groupmod_id = user_data[3]

    dpg.fit_axis_data(x_axis)
    dpg.fit_axis_data(y_axis)
    dpg.set_axis_limits_auto(x_axis)
    dpg.set_axis_limits(y_axis, ymin=0, ymax=500)

    times = list(range(0, len(model_pitches), 1))
    configure_item(status, show = True, default_value = "Extracting model pitch...")
    dpg.add_line_series(times, model_pitches, label=model_file_name, parent=y_axis)
    dpg.add_button(label="Delete " + model_file_name, user_data = [dpg.last_item(), model_file_name, groupmod_id], parent=dpg.last_item(), callback=delete_mod_graph)
    configure_item(status, show = True, default_value = "Model pitch extracted!")

def delete_mod_graph(sender, app_data, user_data):
    """Takes in user_data; deletes line series and file upload."""

    delete_item(user_data[0])
    configure_item(status, default_value = f'{user_data[1]}.wav deleted!')
    delete_item(user_data[2])

def delete_upload(sender, app_data, user_data):
    """Takes in user_data; deletes file upload."""

    delete_item(user_data[3])

def play_file(sender, app_data, user_data):
    """Takes in global file_path (derived from model_file_name); plays the sound file."""

    file_path = user_data
    print('FILEPATH:', file_path)

    if file_path != None:  
        configure_item(status, show = True, default_value = "Playing file...")
        playsound(file_path)
        configure_item(status, show = True, default_value = "Done playing!")


def upload_file_cb(sender, app_data, user_data):
    """Uploads selected file; creates model_file_name and file_path; extracts pitch from file_path. Returns model_pitches."""

    # global model_pitches, model_file_name, file_path

    configure_item(status, show = True, default_value = "Uploading...")
    file_path = app_data["file_path_name"]
    print('file_path:', file_path)
    model_file_name = app_data["file_name_buffer"]
    signal = basic.SignalObj(file_path)
    pitches = pYAAPT.yaapt(signal)
    pitches.set_values(pitches.samp_values, len(pitches.values), interp_tech='spline')
    model_pitches = pitches.values
    model_pitches[model_pitches <= 0] = np.nan #masking 0 values with NaN 
    model_pitches = model_pitches[~np.isnan(model_pitches)] #removing NaN vlaues

    groupmod_id = None

    with group(parent = user_nav_bar, before=record) as groupmod_id:
        configure_item(status, show=False)
        dpg.add_text(model_file_name)
        dpg.add_button(label='Play', callback=play_file, user_data=file_path)
        dpg.add_same_line()
        dpg.add_button(label="Extract Model Pitch", callback = plot_model, user_data = [model_file_name, file_path, model_pitches, groupmod_id])
        dpg.add_same_line()
        dpg.add_button(label="Delete", callback = delete_upload, user_data = [model_file_name, file_path, model_pitches, groupmod_id])        
        dpg.add_spacing(count=3)

##### Mic Pitch Callbacks ######

def record_mic(sender, app_data, user_data):
    """Opens PyAudio stream and records user's audio. Writes user's audio into .wav file. Extracts .wav file for mic_pitches."""

    global mic_file_name, mic_pitches, recording_counter

    set_item_theme(r_button, not_enabled)
    set_item_theme(s_button, series_theme)

    p = pyaudio.PyAudio()

    # open stream
    buffer_size = 1024
    pyaudio_format = pyaudio.paInt16
    n_channels = 1
    samplerate = 44100
    stream = p.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)

    if recording_counter == 0:
        recording_counter = 1
    elif recording_counter != 0:
        recording_counter += 1

    path = os.getcwd()
    dir = os.listdir(path)

    print("Current path: ", path)
    print("Current dir: ", dir)    

    mic_file_name = f'Your Input {recording_counter}.wav'
    mic_file_path = os.path.join(tmpdir.name, mic_file_name)
    mic_pitches = []

    print("\nPath: ", path)
    print("Dir path: ", tmpdir.name)
    print("Full mic path: ", mic_file_path, "\n")

    configure_item(rec_status, show=True, default_value = "Recording...")

    while True:
        try:
            audiobuffer = stream.read(buffer_size)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)
            mic_pitches.append(signal)
            if mouse.is_pressed(button='left'):
                break

        except:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(mic_file_path, 'wb')
    wf.setnchannels(n_channels)
    wf.setsampwidth(p.get_sample_size(pyaudio_format))
    wf.setframerate(samplerate)
    wf.writeframes(b''.join(mic_pitches))
    wf.close()

def stop_mic(sender, data):
    """Creates buttons specific to the mic_file_name (e.g.: YourInput1.wav, YourInput2.wav...) upon ending recording."""

    global recording_counter, group_id

    set_item_theme(r_button, series_theme)
    set_item_theme(s_button, not_enabled)
    configure_item(rec_status, show=True, default_value = "Recording completed! \nPlease extract your pitch.")
    configure_item(mic_sep1, show = True)

    mic_file_name = f'Your Input {recording_counter}.wav'
    mic_file_path = os.path.join(tmpdir.name, mic_file_name)

    group_id = None

    with group(parent=user_nav_bar) as group_id:
        dpg.add_text(mic_file_name)
        dpg.add_button(label="Play", callback = play_your_file, user_data = mic_file_path)
        dpg.add_same_line()
        dpg.add_button(label="Extract Your Pitch", callback= your_pitch, user_data=[mic_file_name, group_id, mic_file_path])
        dpg.add_same_line()
        dpg.add_button(label="Delete", callback= delete_recording, user_data=[mic_file_name, group_id, mic_file_path])
        dpg.add_spacing(count=5)


def play_your_file(sender, app_data, user_data):
    """Each button plays the user_data (aka 'mic_file_path' taken from line 184) specific to it.
    Clicking on this button currently causes the temporary directory to not remove itself. """

    global times
    configure_item(rec_status, show=True, default_value = "Playing...")

    chunk = 1024  
    f = wave.open(user_data,"rb")  
    p = pyaudio.PyAudio()  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    data = f.readframes(chunk)  

    while data:  
        stream.write(data)  
        data = f.readframes(chunk)

    stream.stop_stream()  
    stream.close()  
    p.terminate()  
    
    configure_item(rec_status, show=True, default_value = "Done playing!")

def your_pitch(sender, app_data, user_data):
    """Takes in user_data (aka 'mic_file_name' which points to specific .wav file). 
    Extracts .wav file as mic_pitch. 
    dtwalign module warps mic_pitch to model_pitch for overlapping purposes.
    Warping process prone to IndexError; solution is to shorten recording time. """

    global model_pitches

    configure_item(rec_status, show=True, default_value = "Extracting your pitch...")

    signal = basic.SignalObj(user_data[2])
    pitches = pYAAPT.yaapt(signal)
    pitches.set_values(pitches.samp_values, len(pitches.values), interp_tech='spline')
    mic_pitches = pitches.values
    mic_pitches[mic_pitches <= 0] = np.nan #masking 0 values with NaN 
    mic_pitches = mic_pitches[~np.isnan(mic_pitches)] #removing nan vlaues
    print(len(mic_pitches))

    try:
        times = list(range(0, len(mic_pitches), 1))
        mic_file_name2 = mic_file_name.replace(".wav", "")

        dpg.fit_axis_data(x_axis)
        dpg.fit_axis_data(y_axis)
        dpg.set_axis_limits_auto(x_axis)
        dpg.set_axis_limits(y_axis, ymin=0, ymax=500)

        configure_item(rec_status, show=True, default_value = "Your pitch extracted!")
        dpg.add_line_series(times, mic_pitches, label = mic_file_name2, parent=y_axis)
        dpg.add_button(label="Delete " + mic_file_name2, user_data = [dpg.last_item(), group_id], parent=dpg.last_item(), callback=delete_mic_graph)
        configure_item(rec_status, show=False)

    except AttributeError:
        configure_item(rec_status, default_value = "Please extract model pitch first.")
        delete_item(group_id)

    except IndexError:
        configure_item(rec_status, default_value = "Recording too long. \nPlease try again.")
        delete_item(group_id)

def delete_mic_graph(sender, app_data, user_data):
    """Deletes user's graph and user's mic input."""
    

    delete_item(user_data[0])
    delete_item(user_data[1])

def delete_recording(sender, app_data, user_data):
    """Deletes user's graph and user's mic input."""

    delete_item(user_data[1])

###### Nav Bar Settings ######

with dpg.file_dialog(directory_selector=False, show = False, callback=upload_file_cb) as file_dialog_id:
    dpg.add_file_extension(".wav")
    
with dpg.window(label="User NavBar", width=299, height=900, pos=[0,0]) as user_nav_bar:
    welcome = dpg.add_text("Tone Training")
    instructions = dpg.add_text("To start, please upload an audio file.")
    dpg.add_spacing(count=3)
    upload_button = dpg.add_button(label='Upload file', callback= lambda: dpg.show_item(file_dialog_id))
    dpg.add_spacing(count=3)
    dpg.add_separator() 
    status = dpg.add_text(show = False)
    show_model_name = dpg.add_text(show=False)
    play_model = dpg.add_button(show = False, label="Play", callback=play_file)
    dpg.add_same_line()
    model_pitch = dpg.add_button(label="Extract Model Pitch", user_data=m_pitches, callback=plot_model, show=False)
    dpg.add_separator() 
    dpg.add_spacing(count=3)

    record = dpg.add_text("Your Input")
    dpg.add_text("Click on the Record button to start,\nand the Stop button to stop.")
    dpg.add_spacing(count=3)
    r_button = dpg.add_button(label="Record", callback = record_mic)
    dpg.add_same_line()
    s_button = dpg.add_button(label="Stop", callback = stop_mic)
    dpg.add_spacing(count=3)
    rec_status = dpg.add_text(show = False)
    dpg.add_spacing(count=3)
    mic_sep1 = dpg.add_separator(show = False) 

    with dpg.theme() as theme_id:
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (173, 217, 244), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (173, 217, 244), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
  
    dpg.set_item_theme(user_nav_bar, theme_id)
    dpg.set_item_theme(s_button, not_enabled)         
    dpg.set_item_font(welcome, secondary_font)
    dpg.set_item_font(record, secondary_font)

###### Plot Settings ######

with dpg.window(label="Pitch Plot", width=1250, height=900, pos=[300,0]) as plot_window:

    tips = dpg.add_text("   Here are some basic tips:")
    dpg.add_text("      1. Explore the graph with your mouse! Zoom in and out, move up and down.")
    dpg.add_text("      2. Left click on the legend to show/hide a plot.")
    dpg.add_text("      3. Right click on the legend to delete a plot you are done with.")
    dpg.add_spacing(count=5)

    with dpg.plot(label="Intonation Plot", equal_aspects = True, height=600, width=1200):
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="", no_tick_labels = True, no_gridlines=True, no_tick_marks=True)
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="pitch (Hz)", no_tick_labels = False)

    with dpg.theme() as theme_plot:
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (71, 108, 155), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (71, 108, 155), category=dpg.mvThemeCat_Core)
    
    dpg.set_item_theme(plot_window, theme_plot)
    dpg.set_item_font(tips, secondary_font)

dpg.start_dearpygui()

# after app is done, force cleanup of temp folder
print("Trying to clean up temp folder", tmpdir.name)
try:
    tmpdir.cleanup()
except Exception as e:
    print(e, "- please remove folder manually!")