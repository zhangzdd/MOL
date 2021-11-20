from Ui_frame import Ui_MainWindow
#from settings import setting
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QFileDialog

from threading import Thread
import time
from scipy import signal
from integrated_client import ensemble
import threading

task = []
for b in ['站着','坐着']:
    for pos in range(9):
        for device in range(6):
            for t in range(3):
                for c in ['开始','结束']:
                    task.append(b+" 位置"+str(pos)+" 设备"+str(device)+" 第"+str(t)+"次 "+c)

for b in ['站着','坐着']:
    for device in ["手机","手表"]:
        for hand in ["左手握", "右手握持"]:
            for d in "南东北西":
                for t in range(5):
                    for c in ["开始","结束"]:
                        task.append(b+" "+device+" "+hand+"手机 面朝"+d+" 第"+str(t)+"次 "+c)

task+=["Error!!!"]*1000

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.backend = ensemble()
        self.add_device_button.clicked.connect(self.add_dev)
        self.start_record_button.clicked.connect(self.start_rec)
        self.time_stamp_button.clicked.connect(self.stamp)
        self.list_dev_button.clicked.connect(self.list_dev)
        self.end_rec_button.clicked.connect(self.end_rec)
        self.retrieve_button.clicked.connect(self.retrieve_data)
        self.reboot_button.clicked.connect(self.reboot)
        self.default_dev_button.clicked.connect(self.default_dev)
        self.discard_stamp.clicked.connect(self.discard)
        self.inqurie_thread = threading.Thread(target=self.inquiry)

        self.count = 0

    def inquiry(self):
        while True:
            self.backend.inquire()
            time.sleep(30)
            

    def add_dev(self):
        print(self.device_ip.text())
        self.backend.add_proxy(self.device_ip.text())
        
    
    def discard(self):
        self.backend.discard()
        self.count -= 1
        print("Back to {}".format(task[self.count]))

    def default_dev(self):
        default_dev = [
            "192.168.0.183",
            "192.168.0.178",
            "192.168.0.175",
            "192.168.0.179",
            "192.168.0.139",
            "192.168.0.153"
        ]
        for dev in default_dev:
            self.backend.add_proxy(dev)

    def start_rec(self):
        self.backend.record(self.experiment_name.text(),int(self.duration.text()))
        self.inqurie_thread.start()


    def stamp(self):
        self.backend.stamp()
        self.count += 1
        print(self.count,task[self.count]) 

    def list_dev(self):
        for i,info in enumerate(self.backend.info):
            #print(self.backend.device[i])
            print(self.backend.proxys[i])
            print(info)
    
    def end_rec(self):
        self.backend.end_recording(self.experiment_name.text())
        self.count = 0

    def retrieve_data(self):
        self.backend.retrieve()

    def reboot(self):
        self.backend.reboot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
            