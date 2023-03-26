import bluetooth
import mp3

BLE_MSG = ""
" test"

class ESP32_BLE():
    def __init__(self, name):
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def ble_irq(self, event, data):
        global BLE_MSG
        if event == 1:  # _IRQ_CENTRAL_CONNECT 手机链接了此设备
            mp3.mp3_play('connect')  # 播放连接成功的语音
            self.advertiser()
        elif event == 3:  # _IRQ_GATTS_WRITE 手机发送了数据
            buffer = self.ble.gatts_read(self.rx)
            BLE_MSG = buffer.decode('UTF-8').strip()

    def register(self):
        service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        reader_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        sender_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        services = (
            (
                bluetooth.UUID(service_uuid),
                (
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY),
                    (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
                )
            ),
        )

        ((self.tx, self.rx,),) = self.ble.gatts_register_services(services)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")


# 返回蓝牙接收到的数据
def read():
    return BLE_MSG


# 主函数
def blue_connect(name):
    ble = ESP32_BLE(name)

    return ble


if __name__ == "__main__":
    blue_connect('ESP32')
