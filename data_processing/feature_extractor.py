from frequency_utils import *
import matplotlib.pyplot as plt
from scipy import signal
import os
import time
from numba import jit
from data_read import *

def frequency_feature(feature_dict,time_amplitude_series,sample_rate):
    s = np.array(time_amplitude_series)
    try:
        s = s[:,1:4]
        s = np.mean(s,axis=1)
    except:
        pass
    f = freq(s,sample_rate)

    high_freq_energy = f.band_energy([3750,float("inf")])
    low_freq_energy = f.band_energy([0,3750])
    HLBR = high_freq_energy/low_freq_energy
    one_degree_coefficient = f.binned_spectrum(order=1)
    three_degree_coefficient = f.binned_spectrum(order=3)
    
    feature_dict["hfe"] = high_freq_energy
    feature_dict["lfe"] = low_freq_energy
    feature_dict["HLBR"] = HLBR
    feature_dict["coe_1"] = one_degree_coefficient
    feature_dict["coe_3"] = three_degree_coefficient

def crispness(feature_dict,time_amplitude_series,sample_rate):
    arrayed_series = np.array(time_amplitude_series)

    peaks,properties = signal.find_peaks(arrayed_series)
    """
    max_peak = time_amplitude_series[0]
    peak_within_10ms = []
    for peak in peaks:
        if peak/sample_rate < 0.01:
            peak_within_10ms.append(time_amplitude_series[peaks[peak]])
    peak_within_10ms = np.array(peak_within_10ms)
    feature_dict["peak_ratio_1"] = max_peak/np.mean(peak_within_10ms)
    """
    
    max_peak = time_amplitude_series[0]
    mean_peak_height = np.mean(time_amplitude_series[peaks[0:10]])
    peak_ratio_2 = max_peak/mean_peak_height
    feature_dict["peak_ratio_2"] = peak_ratio_2

    feature_dict["std"] = np.std(arrayed_series,ddof=1)
    feature_dict["area"] = np.sum(arrayed_series)


def autocorr(s1):
    try:
        s = np.array(s1)[:,1:4]
        s = np.mean(s,axis=1)
    except:
        s = np.array(s1)
    
    length = s.size
    #print(length)
    s_reverse = np.zeros(length*2)
    s_reverse[length//2:length//2+length] = s 
    result = signal.fftconvolve(s, s_reverse[::-1], mode='valid')
    
    #result = np.correlate(s, s, mode='same')
    result = result/result[result.argmax()]
    """
    plt.figure()
    plt.title("Autocorrelation")
    plt.plot(result[result.size//2:])
    #plt.plot(result)
    plt.show()
    """
    return result[result.size//2:]


def reach_bottom(path):
    bottom_path_list = []
    aux_queue = [(path,None)]
    while(len(aux_queue)>0):
        #print(aux_queue)
        node = aux_queue.pop(0)
        node_path = node[0]
        parent = node[1]
        try:
            childs = os.listdir(node_path)
            #print(childs)
            for child in childs:
                aux_queue.append((os.path.join(node_path,child),node_path))
        except:
            if parent not in bottom_path_list:
                bottom_path_list.append(parent)
    
    return bottom_path_list


def batch_extract(given_path,data_loader_type):
    bottom_path_list = reach_bottom(given_path)
    #print(bottom_path_list)
    x = []
    y = []
    data_loader = data_loader_type
    for folder in bottom_path_list:
        d = data_loader(folder)
        print("folder "+folder)
        for i in range(0,d.size):
            print(str(i+1)+" of "+str(d.size))
            fd = {}
            ts,sp,lb = d[i]
            crispness(fd,autocorr(ts),sp)
            frequency_feature(fd,ts,sp)
            """
            try:
                #以防有的音频文件不完整
                crispness(fd,autocorr(ts),sp)
                frequency_feature(fd,ts,sp)
            except:
                continue
            """
            feature = []
            for key in fd.keys():
                try:
                    feature.extend(list(fd[key]))
                except:
                    feature.append(fd[key])
            
            #去除捂嘴说话这一极大干扰
            #if lb["pose"] == "hand_cover":
            #    continue

            x.append(feature)
            y.append(str(lb["facing_angle"]))

    return x,y

if __name__ == "__main__":
    start_time = time.time()
    x,y = batch_extract("E:\GIX\data",data_loader_type=data_loader_figlab)
    end_time = time.time()
    print("Time cost "+str(end_time-start_time))