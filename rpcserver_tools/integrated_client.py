import xmlrpc
from xmlrpc import client
import os
import time

class ensemble:
    def __init__(self):
        self.ip = []
        self.proxys = []
        self.ip_device_projection = {}
        self.device_indexes = []
        self.info = []
        self.device = []
        self.rpc_instance = []
        pass
    
    def add_proxy(self,ip):
        new_proxy = client.ServerProxy("http://{}:8000/".format(ip))
        self.proxys.append(new_proxy)
        self.ip.append(ip)
        self.info.append(new_proxy.get_audio_information())
        device_name = self.info[-1].split("\n")[-1]
        self.ip_device_projection[ip] = device_name
        self.device.append(device_name)
    
    def setup_device(self):
        pass


    def record(self,name):
        for i,proxy in enumerate(self.proxys):
            proxy.init()
            proxy.start("./storage/{}.wav".format(name))
        pass

    def end_recording(self):
        for proxy in self.proxys:
            proxy.output()

    def retrieve(self):
        for i,proxy in enumerate(self.proxys):
            print("Retrieving {}".format(proxy))
            file_path = "./storage/{}".format(self.device[i]+self.ip[i])
            os.mkdir(file_path)
            #proxy.do("cd storage")
            file_list = proxy.do("ls ./storage").split("\n")
            print(file_list)
            for file in file_list[:-1]:
                handle = open("{}/{}".format(file_path,file), "wb") 
                handle.write(proxy.file_transfer("./storage/{}".format(file)).data) 
                handle.close()
    
    def stamp(self):
        for proxy in self.proxys:
            proxy.time_stamp()


if __name__ == "__main__":
    colony = ensemble()
    colony.add_proxy("192.168.0.178")
    #print([str(getattr(colony,i)) for i in dir(colony) if not callable(i)])
    print(colony.info[0])
    colony.record()
    time.sleep(8)
    colony.retrieve()