import pyaudio
import numpy as np
from scipy.io import wavfile
import noisereduce as nr
import PySimpleGUI as sg

# Set the parameters for the audio stream
CHUNK = 1024 # Number of frames per buffer
FORMAT = pyaudio.paInt16 # Audio format (16-bit integer)
CHANNELS = 1 # Number of audio channels (mono)
RATE = 21050 # Sampling rate in Hz

# Initialize PyAudio
p = pyaudio.PyAudio()

device_index = ''
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info['name'] == 'CABLE Input (VB-Audio Virtual C':
        #print(device_info)
        device_index = device_info['index']

layout = [
    [sg.Text('Simple noise cancellation')],
    [sg.Drop(values=)],
    [sg.Button('swooce'), sg.Exit()]
]

window = sg.Window('Simple Noise Cancellation Tool', layout)

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Open the speaker stream
output_stream = p.open(format=FORMAT,
                       channels=1,
                       rate=RATE,
                       output=True,
                       output_device_index=device_index)

noiserate, noisedata = wavfile.read("myMicNoise2.wav")

# Start the audio stream loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    #output_stream.write(input_data)

    # Read audio input from the microphone
    input_data = stream.read(CHUNK)

    # Convert the raw bytes to numpy array which reduce_noise() will accept.
    input_buffer = np.frombuffer(input_data, dtype=np.int16)

    reduced_noise = nr.reduce_noise(y=input_buffer, sr=RATE, y_noise=noisedata, n_fft=256, n_std_thresh_stationary=.5, stationary=True)
    output_stream.write(reduced_noise.astype(np.int16).tobytes())



# Clean up the audio streams and PyAudio
stream.stop_stream()
stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()
window.close()
