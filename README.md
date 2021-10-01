# Pitch Noodle (User's Guide)

This is a simple intonation app that extracts, draws, and overlays a learner's pitch on top of a model speaker's pitch. The goal of this app is to help language learners recognize the difference in pitch movements in order to better help them learn the pitch of the language they are learning. For monosyllabic or short tokens, use Pitch training; for longer sentences, use Intonation training.

# Requirements 
Here are a list of requirements needed to run the program. No specific versions needed; just download the latest ones. These requirements are also listed in Requirements.txt

* numpy
* AMFM-decompy
* aubio
* DearPyGUI
* PyAudio
* playsound
* Wave

# Running as .exe file (recommended)
First download this as a zip file and extract it to your computer.
* If working with pitch, click on the Pitch training folder then lauch the the Pitch.exe file. 
* If working with intonation, click on the Intonation training folder then launch the Intonation.exe file. 
This should run the application on your computer without the need to install anything else. 
Note: This does not work on a Mac and has only been tested on Windows 10. 

# Running as .py file
The only file you need to run in Pitch.py or Intonation.py. Use pip to install all required third-party packages listed above: `pip -r requirements.txt`

If using an IDE such as Visual Studio Code or Sublime, simply run the main.py file

If you don't have an IDE: 
* Open up the terminal on your computer
* cd to the appropirate folder (e.g. cd /Users/aprilmelody/Desktop/PythonIntonationApp)
* type in python Pitch.py 

# Tutorial Walkthrough
Using the application is simple! Here's a step-by-step:
* First, upload a .wav file of a model speaker
* Then, click on "extract pitch" to see the model speaker's pitch movement
* Take note of the model speaker's pitch movements and record yourself saying the same sentence using the 'record' and 'stop' buttons. Please make sure you have a microphone on your device!
* Finally, click on "extract your pitch" to see an overlay of your pitch on top of the model speaker's speech 
* Have fun!

Tips:
* Zoom in or zoom out on the graph by using the mouse wheel button
* Show/hide a plot by clicking on the legend
* Delete a plot you no longer want by right clicking on the legend
* Right click on the graph for a whole bunch of other options

# Known Issues
* Longer sentences are tricky and the application might not pick up every voiced segment

# Future Work
* A vline series that shows users at which point of the pitch contour they are at when playing the file
* Ability to scrub back and forth to play only specific parts of the audio file
