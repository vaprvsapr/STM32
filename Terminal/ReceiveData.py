import struct


class OnRead:
    def __init__(self, _ui, _serial):
        self.ui = _ui
        self.serial = _serial

    def __call__(self, *args, **kwargs):
        rx = self.serial.readLine()
        received_data = struct.unpack('<cdc', rx)

        if received_data[0] == b'\x7E' and received_data[2] == b'\xAB':
            message = "Received data: " + str(received_data[1])
            print(message)
            self.ui.LogTransmittedData.append(message)
