from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
import struct

app = QtWidgets.QApplication([])
ui = uic.loadUi("terminal.ui")
ui.setWindowTitle("STM32Terminal")

serial = QSerialPort()
serial.setBaudRate(115200)

portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())

ui.comL.addItems(portList)


def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)
    print("The channel is opened")


def onClose():
    serial.close()
    print("The channel is closed")


def onRead():
    rx = serial.readLine()
    print(rx)


def ledControl(val):
    print(val)


def ledControlRed(val):
    buf: bytes = b'\x7E\xA1\xAB'
    serial.write(buf)
    print(buf)


def sendData():
    data = ui.data.displayText()
    first = b'\x7E'
    last = b'\xAB'
    pack_obj = struct.pack('<cdc', first, float(data), last)

    print('data: ', type(float(data)), float(data))

    print('transmitted pack: ', pack_obj)
    serial.write(pack_obj)


serial.readyRead.connect(onRead)
ui.OpenB.clicked.connect(onOpen)
ui.CloseB.clicked.connect(onClose)

ui.Red.stateChanged.connect(ledControlRed)
ui.Blue.stateChanged.connect(ledControl)
ui.Green.stateChanged.connect(ledControl)

ui.pushButton.clicked.connect(sendData)


ui.show()
app.exec()
