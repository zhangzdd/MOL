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

    def add_dev(self):
        print(self.device_ip.text())
        self.backend.add_proxy(self.device_ip.text())
        
    
    def start_rec(self):
        self.backend.record(self.experiment_name.text())

    def stamp(self):
        self.backend.stamp()

    def list_dev(self):
        for i,info in enumerate(self.backend.info):
            #print(self.backend.device[i])
            print(self.backend.proxys[i])
            print(info)
    
    def end_rec(self):
        self.backend.end_recording()

    def retrieve_data(self):
        self.backend.retrieve()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
            