from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort

from ChannelControl import *
from ReceiveData import *

app = QtWidgets.QApplication([])
path = "c:\Charm\STM32\GraphicUserInterface\GUI.ui"
ui = uic.loadUi(path)
ui.setWindowTitle("Terminal")

serial = QSerialPort()
serial.setBaudRate(115200)
port_list = []

ButtonUpdateChannelList(_ui=ui, _port_ist=port_list)()

serial.readyRead.connect(OnRead(_ui=ui, _serial=serial))
ui.ButtonTransmit.clicked.connect(ButtonTransmitData(_ui=ui, _serial=serial))
ui.ButtonOpenClose.clicked.connect(ButtonOpenClose(_ui=ui, _serial=serial))
ui.ButtonUpdateChannelList.clicked.connect(ButtonUpdateChannelList(_ui=ui, _port_ist=port_list))

ui.show()
app.exec()
