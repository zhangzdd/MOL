from data_read import data_loader
from pyroomacoustics.experimental.localization import tdoa

def gcc_phat_tdoa(feature_dict,time_series,pairs):
    iterlist = []
    gcc_phat = []
    for i in range(0,pairs):
        iterlist.append(time_series[:,i])
    for i in range(0,pairs):
        if (i+1)==pairs:
            break
        for j in range(i+1,pairs):
            print(type(j))
            delay = tdoa(iterlist[i],iterlist[j])
            gcc_phat.append(delay)
    feature_dict["tdoa"] = gcc_phat

if __name__ == "__main__":
    d = data_loader("E:\GIX\sample")
    #ts1,sr1,lb1 = d[0]
    ts2,sr2,lb2 = d[1]
    fd = {}
    gcc_phat_tdoa(fd,ts2,6)
    print(fd)