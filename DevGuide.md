# GUI
The GUI used for this program is DearPyGui. Here are some helpful links if you ever need to tailor this for your purposes: 
* Wiki: https://hoffstadt.github.io/DearPyGui/
* API Documentation: https://hoffstadt.github.io/DearPyGui/

DearPyGUI uses widgets. Everything in the program, from buttons to plots, is a widget with its own unique ID. These widgets pass information back and forth from widget to function via the 'user_data' variable in its arguments. If you need to pass more than one object, use a list!

# pYAAPT
This module is responsible for extracting the pitch of the .wav files, which will then be passed on to the next module (dtwalign) as an array. Note that there are many settings available to developers in order to tweak the final result of the extracted pitch. The documentation for this package can be found here: http://bjbschmitt.github.io/AMFM_decompy/pYAAPT.html 

# dtwalign
A dynamic time warping (dtw) module that this program uses to align recordings of different lengths. This program does throws an error if the user's input is much longer than the model input. The accuracy of the aligning has not been tested and should be high on the priority list. Their homepage has a comprehensive guide on the computational mathematics behind it. https://dynamictimewarping.github.io/

# pyAudio
This module is responsible for reading, writing, and playing all .wav files in this program. Note that it is necessary to use pyAudio to open and close files. Without closing an audio file, the temporary directory will not be deleted when the program exits. Here is some documentation you might find helpful: http://people.csail.mit.edu/hubert/pyaudio/
