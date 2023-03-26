import time
from umqttsimple import MQTTClient

# 全局变量
mqtt_msg = {}


# 回调函数，收到服务器消息后会调用这个函数
def add_msg(topic, msg):
    mqtt_msg[topic] = msg  # 将接受到的数据加入到数据字典中


# 连接mqtt服务器
def mqtt_connect(name, ip, port):
    # 创建mqt
    # esp32的设备名称 MQTT服务器IP地址 MQTT服务器端口
    mqtt_object = MQTTClient(name, ip, port)  # 建立一个MQTT对象
    mqtt_object.set_callback(add_msg)
    mqtt_object.connect()  # 建立连接

    return mqtt_object


# 接收mqtt服务器消息
def get_msg(mqtt_object, topic):
    # 循环检测服务器主题
    for each in topic:
        mqtt_object.subscribe(each.encode())  # 监控主题，接收控制命令
        mqtt_object.check_msg()  # 设置函数回调函数
        time.sleep(0.1)

    return mqtt_msg


# 发送主题数据
def send_msg(mqtt_object, topic, msg):
    # 循环检测服务器主题
    mqtt_object.publish(topic, str(msg))  # 发布主题

    return True


if __name__ == '__main__':
    a = mqtt_connect('ESP32', '192.168.1.56')
    send_msg(a, 'state_dic', 'True')
    print(a)
