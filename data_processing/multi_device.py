from feature_extractor import *
import numpy as np
class Device:
    def __init__(self,model,sample_rate,) -> None:
        self.sample_rate = sample_rate
        self.model = model
        pass
    
    def single_model_judgement(self,time_series):
        fd = {}
        sp = self.sample_rate
        ts = time_series
        crispness(fd,autocorr(ts),sp)
        frequency_feature(fd,ts,sp)
        feature = []
        for key in fd.keys():
            try:
                feature.extend(list(fd[key]))
            except:
                feature.append(fd[key])    
        result = self.model.predict_proba(feature)
        return result
    
    def customized_judgement(self,features):
        pass


class MultiDeviceSys:
    def __init__(self,device_list,device_weight):
        self.device_list = device_list
        self.device_weight = device_weight
    
    def union_vote(self,time_series):
        votes = []
        for device in self.device_list:
            votes.append(device.single_model_judgement(time_series))
        votes = np.array(votes)
        device_weight = np.array(self.device_weight)
        weighted_votes = device_weight*votes
        for i in range(0,len(votes)):
            print(self.device_list[i]+" voted "+str(votes[i]))
        return self.device_list[np.argmax(weighted_votes)]

if __name__ == "__main__":
    model = None
    linear = Device(model,44100)
    square = Device(model,44100)
    double_sys = MultiDeviceSys([linear,square],[1,1])
    time_series = None
    double_sys.union_vote(time_series)