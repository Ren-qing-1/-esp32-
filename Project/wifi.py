import time
import network
from socket import *

wifi_link = False  # wifi连接成功标志位


# 连接wifi
def do_connect(name, password, out_time):
    global wifi_link
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('网络连接中...')
        wlan.connect(name, password)
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
            if i > (out_time - 1):
                print('连接失败')
                return False

    print(wlan.ifconfig())
    wifi_link = True

    return True


# 请求数据
def send_data(send_data):
    # 创建udp套接字
    udp_socket = socket(AF_INET, SOCK_DGRAM)

    # 准备接收方的地址
    dest_addr = ('192.168.1.56', 8080)

    # 发送数据到电脑上
    udp_socket.sendto(send_data.encode('utf-8'), dest_addr)

    # 等待接收1024个字节的数据
    rev_data = udp_socket.recvfrom(1024)

    # 关闭套接字
    udp_socket.close()

    # 接收到的数据rev_data是一个元组
    # 第1个元素是对方发送的数据
    # 第2个元素是对方的ip和端口
    return rev_data[0]


if __name__ == '__main__':
    if do_connect('ChinaNet-4mwW', 'qh37eev9'):
        send_data('你好')
