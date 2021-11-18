import os
from scipy.io.wavfile import read,write
import numpy as np
from abc import ABCMeta, abstractmethod
from scipy import signal

class base_data_read:
    __metaClass__ = ABCMeta
    def __init__(self,path):
        self.time_series = []
        self.sample_rate = []
        self.label = []
        for item in os.listdir(path):
            #print(item)
            #print(type(item))
            rate,series = read(os.path.join(path,item))
            if int(np.max(series))<1:
                #(item)
                continue
            self.time_series.append(series)
            self.sample_rate.append(rate)
            self.label.append(self.parse(item))
        self.size = len(self.sample_rate)
    
    @abstractmethod
    def parse(self,audio_label):
        pass

    def __getitem__(self, key):
        return self.time_series[key],self.sample_rate[key],self.label[key]
"""
class data_loader:
    def __init__(self,path) -> None:
        self.time_series = []
        self.sample_rate = []
        self.label = []
        for item in os.listdir(path):
            #print(item)
            #print(type(item))
            rate,series = read(os.path.join(path,item))
            self.time_series.append(series)
            self.sample_rate.append(rate)
            self.label.append(self.parse(item))
        self.size = len(self.sample_rate)

    def parse(self,audio_label):
        label_dict = {}
        digit_label = audio_label.split(".")[0]
        
        if digit_label[3] == "0":
            label_dict["gender"] = "male"
        else:
            label_dict["gender"] = "female"
        
        if digit_label[4:6] == "01":
            label_dict["channels"] = "six"
        else:
            label_dict["channels"] = "four"

        if digit_label[6:8] == "01":
            label_dict["location"] = "4-511"
        else:
            label_dict["location"] = "4-527"

        if digit_label[8:10] == "01":
            label_dict["standing_angle"] = 0
        elif digit_label[8:10] == "02":
            label_dict["standing_angle"] = 45
        elif digit_label[8:10] == "03":
            label_dict["standing_angle"] = 90

        label_dict["distance"] = int(digit_label[10:12])
        label_dict["facing_angle"] = int(digit_label[12:15])

        return label_dict
    
    def __getitem__(self, key):
        return self.time_series[key],self.sample_rate[key],self.label[key]
"""
class data_loader_local(base_data_read):
    def __init__(self,path):
        super().__init__(path)
        self.resample()

    def parse(self,audio_label):
        label_dict = {}
        digit_label = audio_label.split(".")[0]
        
        if digit_label[3] == "0":
            label_dict["gender"] = "male"
        else:
            label_dict["gender"] = "female"
        
        if digit_label[4:6] == "01":
            label_dict["channels"] = "six"
        else:
            label_dict["channels"] = "four"

        if digit_label[6:8] == "01":
            label_dict["location"] = "4-511"
        else:
            label_dict["location"] = "4-527"

        if digit_label[8:10] == "01":
            label_dict["standing_angle"] = 0
        elif digit_label[8:10] == "02":
            label_dict["standing_angle"] = 45
        elif digit_label[8:10] == "03":
            label_dict["standing_angle"] = 90

        if digit_label[15:17] == "02":
            label_dict["pose"] = "hand_cover"
        else:
            label_dict["pose"] = "none_cover"
        
        label_dict["distance"] = int(digit_label[10:12])
        label_dict["facing_angle"] = int(digit_label[12:15])

        return label_dict

    def resample(self,target_samplerate=48000):
        new_series = []
        new_rate = []
        for i in range(0,len(self.time_series)):
            secs = len(self.time_series[i])/self.sample_rate[i]
            samps = int(target_samplerate*secs)
            new_series.append(signal.resample(self.time_series[i],samps))
            new_rate.append(target_samplerate)
        self.time_series = new_series
        self.sample_rate = new_rate


class data_loader_figlab(base_data_read):
    def parse(self,audio_label):
        label_dict = {}
        digit_label = audio_label.split("_")
        label_dict["facing_angle"] = int(digit_label[1])
        
        return label_dict



if __name__ == "__main__":
    d = data_loader_local(r"E:\GIX\sample_root\Sat Jul  3 09 59 46 20211")
    #d.resample(48000)
    f = data_loader_figlab(r"E:\GIX\figlab_data\s1\s1_downstairs_nowall_trial1\A0_1_0")
    #print(d.label)
    print(d.time_series[0].shape)
    print(d.sample_rate[0])
    print(f.time_series[0].shape)
    print(f.sample_rate)
    print("Success")