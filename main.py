import matplotlib.pyplot as plt
from mic_pitch import cleaned_mic_pitches
from model_pitch import cleaned_pitches, times

plt.style.use('seaborn-pastel')

plt.plot(times, cleaned_pitches, linewidth=2.0)
plt.plot(times, cleaned_mic_pitches, linewidth=2.0)
plt.xlabel('Time(ms)')
plt.ylabel('Pitch (Hz)')
plt.title('Pitch contour comparison')

plt.show()
