from xmlrpc.server import SimpleXMLRPCServer 
import xmlrpc
import pyaudio
import wave
import threading
import os
import time

def get_audio_information():
    pobj = pyaudio.PyAudio()
    info = pobj.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    response = []
    for i in range(0, numdevices):
        if (pobj.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            response.append("Input Device id "+str(i)+ " - "+pobj.get_device_info_by_host_api_device_index(0, i).get('name'))
            device_info = pobj.get_device_info_by_host_api_device_index(0, i).get('name')
            respeaker_index = i
            if "seeed" in device_info:
                device = device_info.split(":")[0]
    else:
        response.append("Output Device id "+str(i)+ " - "+pobj.get_device_info_by_host_api_device_index(0, i).get('name'))
    
    response.append(device)
    return "\n".join(response)
    pass


def file_transfer(filename): 
     handle = open(filename,'rb') 
     encoded_file = xmlrpc.client.Binary(handle.read()) 
     handle.close() 
     return encoded_file


        

def do(order):
    fd = os.popen(order)
    print(type(fd))
    #print(fd.readlines())
    lines_list = fd.readlines()
    response = "".join(lines_list)
    #print(response)
    return response

class recorder:
    def init(self,rate=48000,channel=2,width=2,index=2,chunk=1024,length=120):
        self.rate = rate
        self.channel = channel
        self.width = width
        self.index = index
        self.chunk = chunk
        self.length = length
        self.recording_obj = pyaudio.PyAudio()
        self.frame = []
        self.on_recording = False
        self.stamp_string = []
        #server.register_instance(self)
        pass
    
    def current_state(self):
        attr_list = [str(getattr(self,i)) for i in dir(self) if not callable(getattr(self, i))]
        return ",".join(attr_list)
        pass
    
    def start(self,name="test_instance.wav"):
        print("Rate {}".format(self.rate))
        print("start recording")
        self.start_time = time.time()
        #self.stamp_string.append("{}/n".format(str(self.start_time())))
        self.stream = self.recording_obj.open(
            rate=self.rate,
            channels=self.channel,
            format=self.recording_obj.get_format_from_width(self.width),
            input=True,
            input_device_index=self.index
        )
        self.record_thread = threading.Thread(target=self.record,args=(name,))
        self.on_recording = True
        self.record_thread.start()
        
        pass
    
    def time_stamp(self):
        current_time = time.time()
        stamp = current_time - self.start_time
        self.stamp_string.append("{}\n".format(str(stamp)))
        pass

    def end_rec(self):
        self.on_recording = False

    def record(self,name):
        print("Thread started")
        print(self.on_recording)
        self.clear()
        for i in range(0,int(self.rate*self.length/self.chunk)):
            #print(self.on_recording)
            data = self.stream.read(self.chunk,exception_on_overflow=False)
            self.frame.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.recording_obj.terminate()
        
        wf = wave.open(name,"wb")
        wf.setnchannels(self.channel)
        wf.setsampwidth(self.recording_obj.get_sample_size(self.recording_obj.get_format_from_width(self.width)))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frame))
        wf.close()
        
        file_handle = open("{}_stamp.txt".format(name),"w")
        file_handle.writelines(self.stamp_string)
        file_handle.close()

        self.clear()
        self.on_recording = False
        print("record ended")

    def clear(self):
        self.on_recording = False
        self.frame = []
        self.stamp_string = []

    def output(self,name):
        self.stream.stop_stream()
        self.stream.close()
        self.recording_obj.terminate()
        
        wf = wave.open(name,"wb")
        wf.setnchannels(self.channel)
        wf.setsampwidth(self.recording_obj.get_sample_size(self.recording_obj.get_format_from_width(self.width)))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frame))
        wf.close()
        self.clear()


server = SimpleXMLRPCServer(("192.168.0.178", 8000),allow_none=True) 
print("Listening on port 8000...")
server.register_function(file_transfer,"file_transfer") 
server.register_function(do,"do")
server.register_instance(recorder())
server.register_function(get_audio_information,"get_audio_information")

server.serve_forever()