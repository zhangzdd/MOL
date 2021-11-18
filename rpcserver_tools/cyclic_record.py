import time
import os
import pyaudio
import sys
pobj = pyaudio.PyAudio()
info = pobj.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

starting_time = sys.argv[1]
#starting_time = "10:10:20"

device = ""

for i in range(0, numdevices):
    if (pobj.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", pobj.get_device_info_by_host_api_device_index(0, i).get('name'))
        device_info = pobj.get_device_info_by_host_api_device_index(0, i).get('name')
        respeaker_index = i
        if "seeed" in device_info:
            device = device_info.split(":")[0]
    else:
        print("Output Device id ", i, " - ", pobj.get_device_info_by_host_api_device_index(0, i).get('name'))


directions = [i for i in range(0,360,45)]

while True:
    current_time = time.asctime(time.localtime(time.time())).split(" ")[3]
    if current_time.split(":")[1] == starting_time.split(":")[1]:
        break

for direction in directions:
    name = str(direction) + "_" + device
    print("Record on "+ name)
    os.system("python3 recorder.py " + name)
    time.sleep(7)