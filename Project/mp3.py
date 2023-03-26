import machine
import time

# 指令字典
command_dic = {
    'start': b'\x7e\x02\x01\xef',
    'start': b'\x7e\x04\x41\x00\x04\xef',  # 测试插播语音
    'stop': b'\x7e\x02\x02\xef',
    'next': b'\x7e\x02\x03\xef',
    'last': b'\x7e\x02\x04\xef',
    'up': b'\x7e\x02\x05\xef',
    'down': b'\x7e\x02\x06\xef',
    'connect': b'\x7e\x04\x41\x00\x05\xef',
    'disconnection': b'\x7e\x04\x41\x00\x06\xef'
}


# 播放音乐
def mp3_play(command, index=None):
    if command == 'play':
        bur = command_dic[command] + ('\'x' + index + '\'xef').encode()
    else:
        bur = command_dic[command]

    uart = machine.UART(2, baudrate=9600, rx=26, tx=25, timeout=10)
    uart.write(bur)


if __name__ == '__main__':
    mp3_play('start')
