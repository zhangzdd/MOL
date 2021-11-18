from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import numpy as np
from data_read import data_loader_local
#from numpy import fft,ifft


class freq():
    def __init__(self,time_series,sample_rate) -> None:
        #self.spec_data = 2/sample_rate*abs(fft(time_series))[:sample_rate/2]
        self.spec_data = 2/sample_rate*abs(fft(time_series))[:len(time_series)//2]
        self.time_series = time_series
        self.sample_rate = sample_rate
        #self.fig = plt.figure()
        self.binned_data = None
        self.binned_spectrum()
        
    def band_energy(self,band_tuple):
        low_band, high_band = band_tuple[0], band_tuple[1]
        if high_band == float("inf"):
            return sum(self.spec_data[low_band:])
        else:
            return sum(self.spec_data[low_band:high_band])

    def binned_spectrum(self,bin_size=128,order=2):
        self.binned_data = np.bincount(self.spec_data.astype("int64"),minlength=bin_size)
        return np.polyfit(x=np.arange(len(self.binned_data)),y=self.binned_data,deg=order)

    def show(self):
        ax1 = self.fig.add_subplot(1,2,1)
        ax2 = self.fig.add_subplot(1,2,2)

        ax1.plot(self.spec_data)
        ax1.set_title("spectrum of data")
        ax2.plot(self.binned_data)
        ax2.set_title("binned_spectrum")

        plt.show()


if __name__ == "__main__":
    d = data_loader_local("E:\GIX\sample_root\sample")
    ts,sr,lb = d[1]
    print(lb)
    print(ts[:,0].shape)
    f = freq(ts[:,0],sr)
    a,b = f.binned_spectrum(order=3)[0], f.binned_spectrum()[1]
    print("coe1 "+str(a)+" "+str(b))
    print("Low band energy "+str(f.band_energy((0,3750))))
    print("High band energy "+str(f.band_energy((3750,float("inf")))))
    f.show()
    print("Success")
