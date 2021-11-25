from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import QIODevice
import struct


#  Finished
class ButtonUpdateChannelList:
    def __init__(self, _ui, _port_ist):
        self.ui = _ui
        self.port_list = _port_ist

    def __call__(self, *args, **kwargs):
        self.port_list.clear()
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            self.port_list.append(port.portName())

        for i in range(self.ui.ListChannels.count()):
            self.ui.ListChannels.removeItem(0)
        self.ui.ListChannels.addItems(self.port_list)


is_channel_open = 0


#  Finished
class ButtonOpenClose:
    def __init__(self, _ui, _serial):
        self.ui = _ui
        self.serial = _serial

    def __call__(self, *args, **kwargs):
        global is_channel_open
        if is_channel_open == 0:
            if str(self.ui.ListChannels.currentText()) == "":
                self.ui.LogTransmittedData.append("Error: nothing to open")
            else:
                is_channel_open = 1

                self.serial.setPortName(self.ui.ListChannels.currentText())
                self.serial.open(QIODevice.ReadWrite)
                self.ui.ButtonTransmit.setText("Transmit")
                self.ui.ButtonOpenClose.setText("Close")
                message = "Channel " + \
                          str(self.ui.ListChannels.currentText()) + \
                          " is opened"
                print(message)
                self.ui.LabelChannelInfo.setText(message)
                self.ui.LogTransmittedData.append(message)
        elif is_channel_open == 1:
            is_channel_open = 0

            self.serial.close()
            self.ui.ButtonTransmit.setText("Channel is not opened")
            self.ui.ButtonOpenClose.setText("Open")
            message = "Channel " + str(self.ui.ListChannels.currentText()) + " is closed"
            print(message)
            self.ui.LabelChannelInfo.setText(message)
            self.ui.LogTransmittedData.append(message)


class ButtonTransmitData:
    def __init__(self, _ui, _serial):
        self.ui = _ui
        self.serial = _serial

    def __call__(self, *args, **kwargs):
        data = self.ui.LineDataToTransmit.displayText()

        if not is_channel_open:
            self.ui.ButtonTransmit.setText("Channel is not opened")
            message = "Error: channel is not opened"
            self.ui.LogTransmittedData.append(message)
            print(message)

        if is_channel_open:
            if data == "":
                self.ui.LogTransmittedData.append("Error: nothing to transmit")
            else:
                first = b'\x7E'
                last = b'\xAB'

                pack_obj = struct.pack('<cdc', first, float(data), last)

                print('Data to transmit:', type(float(data)), float(data))
                message = "Transmitted data: " + str(float(data))
                print(message)
                self.ui.LogTransmittedData.append(message)
                self.serial.write(pack_obj)
